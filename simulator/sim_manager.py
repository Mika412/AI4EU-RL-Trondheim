import glob
import os
import shutil
import sys
import time
from pathlib import Path

# sys.path.append("./src")
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from datetime import datetime

from environment.BaseEnv import SumoBaseEnvironment
from environment.modules.CellsModule import CellsModule
from environment.modules.EmissionsModule import EmissionsModule, EmissionType
from environment.modules.EmissionsRendererModule import EmissionsRendererModule
from environment.modules.InductionLoopsModule import InductionLoopsModule
from generate_data import create_detections, create_polys, create_routes
from scripts.download_sensors import download_sensors


class CustomExperiment(SumoBaseEnvironment):
    def __init__(self, env_dir, out_dir=False, use_gui=False, num_seconds=20000):
        super().__init__(env_dir, out_dir, use_gui, num_seconds)

        self.cells = CellsModule(
            self._cell_shapes,
            self._edges_in_cells,
            self.cell_max_height,
            self.cell_max_width,
            self.cell_height,
            self.cell_width,
        )
        self.emissions = EmissionsModule(
            self.cells,
            self.output_dir,
            [EmissionType.NOx],
            update_every=10,
            save_every=10,
            save_to_file=True,
        )
        inductions = InductionLoopsModule(self.output_dir, self._induction_loops)

        # Extra modules
        extra_modules = []
        extra_modules.append(self.cells)
        extra_modules.append(self.emissions)
        extra_modules.append(inductions)

        self.set_extra_modules(extra_modules)


class SimulationManager:
    current_start_date = ""
    current_end_date = ""
    current_perc = 1
    current_map = ""
    env = None

    current_closed_state = {}

    def initialize(self, start_date, end_date, density_perc):
        if (
            self.env
            and start_date == self.current_start_date
            and end_date == self.current_end_date
            and density_perc == self.current_perc
        ):
            self.env.reset()
            return self.get_emissions()

        self.current_start_date = start_date
        self.current_end_date = end_date
        self.current_perc = density_perc

        d1_start_date = datetime.strptime(start_date, "%Y-%m-%d")
        d2_end_date = datetime.strptime(end_date, "%Y-%m-%d")
        n_days = abs((d2_end_date - d1_start_date).days)

        map = "small_extended"
        self.download_data(map, start_date, end_date, density_perc)
        self.env = CustomExperiment(
            env_dir="./simulations/" + map + "/",
            out_dir="./outputs/" + map + "/",
            use_gui=False,
            num_seconds=n_days * 86400,
        )
        self.env.reset()

    def download_data(self, map, start_date, end_date, density_perc):

        # Delete all CSV files
        # TODO: Replace this section to use the shutil library
        dir_name = "./sensors/data/"
        test = os.listdir(dir_name)

        for item in test:
            if item.endswith(".csv"):
                os.remove(os.path.join(dir_name, item))

        shutil.copyfile(
            "./sensors/sensor_location/sensor_location_{}.csv".format(map),
            "./sensors/sensor_location.csv",
        )

        dates_sensor_location = "./sensors/data/{}_{}".format(start_date, end_date)
        sensor_dates_path = Path(dates_sensor_location)
        if sensor_dates_path.exists() and sensor_dates_path.is_dir():
            files = glob.iglob(
                os.path.join(
                    "./sensors/data/{}_{}".format(start_date, end_date), "*.csv"
                )
            )
            for file in files:
                if os.path.isfile(file):
                    shutil.copy2(file, "./sensors/data/")
        else:
            os.makedirs(dates_sensor_location, exist_ok=True)
            download_sensors(
                "./sensors/sensor_location.csv",
                dates_sensor_location,
                start_date,
                end_date,
            )
            files = glob.iglob(
                os.path.join(
                    "./sensors/data/{}_{}".format(start_date, end_date), "*.csv"
                )
            )
            for file in files:
                if os.path.isfile(file):
                    shutil.copy2(file, "./sensors/data/")

        create_detections(
            "./simulations/{}/".format(map), "./sensors/", 86400, density_perc, 0
        )
        create_routes("./simulations/{}/".format(map))
        create_polys("./simulations/{}/".format(map), 3400, 3300, 200, 200)

    def step(self, cell_states, steps):
        if self.has_ended():
            return

        self.change_cell_state(cell_states)

        for i in range(steps):
            self.env.step()
            print(
                "Steps: {}/{} Closed cells: {}/{}".format(
                    int(self.env.sim_step),
                    self.env.sim_max_time,
                    len(self.env.cells.closed_cells),
                    len(self.env.cells.cells_to_edges),
                ),
                end="\r",
            )
            if self.has_ended():
                break

    def get_emissions(self):
        emissions = {}
        for cell_id in self.env.cells.cells_to_edges:
            emission_val = self.env.emissions.get_cell_emissions(
                cell_id, EmissionType.NOx
            )
            emissions[cell_id] = emission_val
        return emissions

    def get_vehicles(self):
        vehicles = {}
        for cell_id in self.env.cells.cells_to_edges:
            car_count = 0
            for edge_id in self.env.cells.cells_to_edges[cell_id]:
                car_count += self.env.traci.edge.getLastStepVehicleNumber(edge_id)
            vehicles[cell_id] = car_count
        return vehicles

    def get_cell_states(self):
        return self.current_closed_state

    def change_cell_state(self, cell_states):
        for cell_id, value in cell_states.items():
            if not cell_id in self.env.cells.cells_to_edges:
                continue
            if value:
                self.env.cells.close_cell(cell_id)
                self.current_closed_state[cell_id] = True
            else:
                self.env.cells.open_cell(cell_id)
                self.current_closed_state[cell_id] = False

    def get_cells_map(self):
        cell_map = {}
        for cell_id in self.env.cells.cells:
           pos = {}
           cell_obj = self.env.cells.cells[cell_id]
           pos['x'] = cell_obj.matrixPosX
           pos['y'] = cell_obj.matrixPosY
           cell_map[cell_id] = pos

        return cell_map
                
    def current_step(self):
        return int(self.env.sim_step)

    def has_ended(self):
        return self.env.is_done
