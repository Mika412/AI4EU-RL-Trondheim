# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: simulator.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='simulator.proto',
  package='isr.simulation',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0fsimulator.proto\x12\x0eisr.simulation\"1\n\x0bInitRequest\x12\x11\n\tStartDate\x18\x01 \x01(\t\x12\x0f\n\x07\x45ndDate\x18\x02 \x01(\t\"!\n\x0cInitResponse\x12\x11\n\tisRunning\x18\x01 \x01(\x08\"\x1f\n\x0bStepRequest\x12\x10\n\x08numSteps\x18\x01 \x01(\x05\"\x1e\n\x0cStepResponse\x12\x0e\n\x06isDone\x18\x01 \x01(\x08\"\x12\n\x10\x45missionsRequest\"\x8a\x01\n\x11\x45missionsResponse\x12\x43\n\temissions\x18\x01 \x03(\x0b\x32\x30.isr.simulation.EmissionsResponse.EmissionsEntry\x1a\x30\n\x0e\x45missionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x02:\x02\x38\x01\"\x95\x01\n\x16\x43hangeCellStateRequest\x12I\n\ncell_state\x18\x01 \x03(\x0b\x32\x35.isr.simulation.ChangeCellStateRequest.CellStateEntry\x1a\x30\n\x0e\x43\x65llStateEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x08:\x02\x38\x01\"\x19\n\x17\x43hangeCellStateResponse2\xd8\x02\n\x08Simulate\x12M\n\x10start_simulation\x12\x1b.isr.simulation.InitRequest\x1a\x1c.isr.simulation.InitResponse\x12\x41\n\x04step\x12\x1b.isr.simulation.StepRequest\x1a\x1c.isr.simulation.StepResponse\x12T\n\rget_emissions\x12 .isr.simulation.EmissionsRequest\x1a!.isr.simulation.EmissionsResponse\x12\x64\n\x11\x63hange_cell_state\x12&.isr.simulation.ChangeCellStateRequest\x1a\'.isr.simulation.ChangeCellStateResponseb\x06proto3'
)




_INITREQUEST = _descriptor.Descriptor(
  name='InitRequest',
  full_name='isr.simulation.InitRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='StartDate', full_name='isr.simulation.InitRequest.StartDate', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='EndDate', full_name='isr.simulation.InitRequest.EndDate', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=35,
  serialized_end=84,
)


_INITRESPONSE = _descriptor.Descriptor(
  name='InitResponse',
  full_name='isr.simulation.InitResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='isRunning', full_name='isr.simulation.InitResponse.isRunning', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=86,
  serialized_end=119,
)


_STEPREQUEST = _descriptor.Descriptor(
  name='StepRequest',
  full_name='isr.simulation.StepRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='numSteps', full_name='isr.simulation.StepRequest.numSteps', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=121,
  serialized_end=152,
)


_STEPRESPONSE = _descriptor.Descriptor(
  name='StepResponse',
  full_name='isr.simulation.StepResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='isDone', full_name='isr.simulation.StepResponse.isDone', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=154,
  serialized_end=184,
)


_EMISSIONSREQUEST = _descriptor.Descriptor(
  name='EmissionsRequest',
  full_name='isr.simulation.EmissionsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=186,
  serialized_end=204,
)


_EMISSIONSRESPONSE_EMISSIONSENTRY = _descriptor.Descriptor(
  name='EmissionsEntry',
  full_name='isr.simulation.EmissionsResponse.EmissionsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='isr.simulation.EmissionsResponse.EmissionsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='isr.simulation.EmissionsResponse.EmissionsEntry.value', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=297,
  serialized_end=345,
)

_EMISSIONSRESPONSE = _descriptor.Descriptor(
  name='EmissionsResponse',
  full_name='isr.simulation.EmissionsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='emissions', full_name='isr.simulation.EmissionsResponse.emissions', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_EMISSIONSRESPONSE_EMISSIONSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=207,
  serialized_end=345,
)


_CHANGECELLSTATEREQUEST_CELLSTATEENTRY = _descriptor.Descriptor(
  name='CellStateEntry',
  full_name='isr.simulation.ChangeCellStateRequest.CellStateEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='isr.simulation.ChangeCellStateRequest.CellStateEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='isr.simulation.ChangeCellStateRequest.CellStateEntry.value', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=449,
  serialized_end=497,
)

_CHANGECELLSTATEREQUEST = _descriptor.Descriptor(
  name='ChangeCellStateRequest',
  full_name='isr.simulation.ChangeCellStateRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cell_state', full_name='isr.simulation.ChangeCellStateRequest.cell_state', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_CHANGECELLSTATEREQUEST_CELLSTATEENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=348,
  serialized_end=497,
)


_CHANGECELLSTATERESPONSE = _descriptor.Descriptor(
  name='ChangeCellStateResponse',
  full_name='isr.simulation.ChangeCellStateResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=499,
  serialized_end=524,
)

_EMISSIONSRESPONSE_EMISSIONSENTRY.containing_type = _EMISSIONSRESPONSE
_EMISSIONSRESPONSE.fields_by_name['emissions'].message_type = _EMISSIONSRESPONSE_EMISSIONSENTRY
_CHANGECELLSTATEREQUEST_CELLSTATEENTRY.containing_type = _CHANGECELLSTATEREQUEST
_CHANGECELLSTATEREQUEST.fields_by_name['cell_state'].message_type = _CHANGECELLSTATEREQUEST_CELLSTATEENTRY
DESCRIPTOR.message_types_by_name['InitRequest'] = _INITREQUEST
DESCRIPTOR.message_types_by_name['InitResponse'] = _INITRESPONSE
DESCRIPTOR.message_types_by_name['StepRequest'] = _STEPREQUEST
DESCRIPTOR.message_types_by_name['StepResponse'] = _STEPRESPONSE
DESCRIPTOR.message_types_by_name['EmissionsRequest'] = _EMISSIONSREQUEST
DESCRIPTOR.message_types_by_name['EmissionsResponse'] = _EMISSIONSRESPONSE
DESCRIPTOR.message_types_by_name['ChangeCellStateRequest'] = _CHANGECELLSTATEREQUEST
DESCRIPTOR.message_types_by_name['ChangeCellStateResponse'] = _CHANGECELLSTATERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

InitRequest = _reflection.GeneratedProtocolMessageType('InitRequest', (_message.Message,), {
  'DESCRIPTOR' : _INITREQUEST,
  '__module__' : 'simulator_pb2'
  # @@protoc_insertion_point(class_scope:isr.simulation.InitRequest)
  })
_sym_db.RegisterMessage(InitRequest)

InitResponse = _reflection.GeneratedProtocolMessageType('InitResponse', (_message.Message,), {
  'DESCRIPTOR' : _INITRESPONSE,
  '__module__' : 'simulator_pb2'
  # @@protoc_insertion_point(class_scope:isr.simulation.InitResponse)
  })
_sym_db.RegisterMessage(InitResponse)

StepRequest = _reflection.GeneratedProtocolMessageType('StepRequest', (_message.Message,), {
  'DESCRIPTOR' : _STEPREQUEST,
  '__module__' : 'simulator_pb2'
  # @@protoc_insertion_point(class_scope:isr.simulation.StepRequest)
  })
_sym_db.RegisterMessage(StepRequest)

StepResponse = _reflection.GeneratedProtocolMessageType('StepResponse', (_message.Message,), {
  'DESCRIPTOR' : _STEPRESPONSE,
  '__module__' : 'simulator_pb2'
  # @@protoc_insertion_point(class_scope:isr.simulation.StepResponse)
  })
_sym_db.RegisterMessage(StepResponse)

EmissionsRequest = _reflection.GeneratedProtocolMessageType('EmissionsRequest', (_message.Message,), {
  'DESCRIPTOR' : _EMISSIONSREQUEST,
  '__module__' : 'simulator_pb2'
  # @@protoc_insertion_point(class_scope:isr.simulation.EmissionsRequest)
  })
_sym_db.RegisterMessage(EmissionsRequest)

EmissionsResponse = _reflection.GeneratedProtocolMessageType('EmissionsResponse', (_message.Message,), {

  'EmissionsEntry' : _reflection.GeneratedProtocolMessageType('EmissionsEntry', (_message.Message,), {
    'DESCRIPTOR' : _EMISSIONSRESPONSE_EMISSIONSENTRY,
    '__module__' : 'simulator_pb2'
    # @@protoc_insertion_point(class_scope:isr.simulation.EmissionsResponse.EmissionsEntry)
    })
  ,
  'DESCRIPTOR' : _EMISSIONSRESPONSE,
  '__module__' : 'simulator_pb2'
  # @@protoc_insertion_point(class_scope:isr.simulation.EmissionsResponse)
  })
_sym_db.RegisterMessage(EmissionsResponse)
_sym_db.RegisterMessage(EmissionsResponse.EmissionsEntry)

ChangeCellStateRequest = _reflection.GeneratedProtocolMessageType('ChangeCellStateRequest', (_message.Message,), {

  'CellStateEntry' : _reflection.GeneratedProtocolMessageType('CellStateEntry', (_message.Message,), {
    'DESCRIPTOR' : _CHANGECELLSTATEREQUEST_CELLSTATEENTRY,
    '__module__' : 'simulator_pb2'
    # @@protoc_insertion_point(class_scope:isr.simulation.ChangeCellStateRequest.CellStateEntry)
    })
  ,
  'DESCRIPTOR' : _CHANGECELLSTATEREQUEST,
  '__module__' : 'simulator_pb2'
  # @@protoc_insertion_point(class_scope:isr.simulation.ChangeCellStateRequest)
  })
_sym_db.RegisterMessage(ChangeCellStateRequest)
_sym_db.RegisterMessage(ChangeCellStateRequest.CellStateEntry)

ChangeCellStateResponse = _reflection.GeneratedProtocolMessageType('ChangeCellStateResponse', (_message.Message,), {
  'DESCRIPTOR' : _CHANGECELLSTATERESPONSE,
  '__module__' : 'simulator_pb2'
  # @@protoc_insertion_point(class_scope:isr.simulation.ChangeCellStateResponse)
  })
_sym_db.RegisterMessage(ChangeCellStateResponse)


_EMISSIONSRESPONSE_EMISSIONSENTRY._options = None
_CHANGECELLSTATEREQUEST_CELLSTATEENTRY._options = None

_SIMULATE = _descriptor.ServiceDescriptor(
  name='Simulate',
  full_name='isr.simulation.Simulate',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=527,
  serialized_end=871,
  methods=[
  _descriptor.MethodDescriptor(
    name='start_simulation',
    full_name='isr.simulation.Simulate.start_simulation',
    index=0,
    containing_service=None,
    input_type=_INITREQUEST,
    output_type=_INITRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='step',
    full_name='isr.simulation.Simulate.step',
    index=1,
    containing_service=None,
    input_type=_STEPREQUEST,
    output_type=_STEPRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_emissions',
    full_name='isr.simulation.Simulate.get_emissions',
    index=2,
    containing_service=None,
    input_type=_EMISSIONSREQUEST,
    output_type=_EMISSIONSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='change_cell_state',
    full_name='isr.simulation.Simulate.change_cell_state',
    index=3,
    containing_service=None,
    input_type=_CHANGECELLSTATEREQUEST,
    output_type=_CHANGECELLSTATERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_SIMULATE)

DESCRIPTOR.services_by_name['Simulate'] = _SIMULATE

# @@protoc_insertion_point(module_scope)