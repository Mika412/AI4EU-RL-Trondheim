class ActorManager:
    default_steps_perform = 10
    EmissionsThreshold = 50

    def get_action(self, emissions, current_step=0):
        cell_state = {}

        for key, value in emissions.items():
            cell_state[key] = value >= self.EmissionsThreshold

        return cell_state, self.default_steps_perform
