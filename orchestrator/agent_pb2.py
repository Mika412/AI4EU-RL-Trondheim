# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: agent.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='agent.proto',
  package='agent',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0b\x61gent.proto\x12\x05\x61gent\"\x88\x01\n\x0bStepRequest\x12\x10\n\x08numSteps\x18\x01 \x01(\x05\x12\x35\n\ncell_state\x18\x02 \x03(\x0b\x32!.agent.StepRequest.CellStateEntry\x1a\x30\n\x0e\x43\x65llStateEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x08:\x02\x38\x01\"\x8e\x01\n\rStateResponse\x12\x13\n\x0b\x63urrentStep\x18\x01 \x01(\x05\x12\x36\n\temissions\x18\x02 \x03(\x0b\x32#.agent.StateResponse.EmissionsEntry\x1a\x30\n\x0e\x45missionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x02:\x02\x38\x01\x32?\n\x05\x41gent\x12\x36\n\nget_action\x12\x14.agent.StateResponse\x1a\x12.agent.StepRequestb\x06proto3'
)




_STEPREQUEST_CELLSTATEENTRY = _descriptor.Descriptor(
  name='CellStateEntry',
  full_name='agent.StepRequest.CellStateEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='agent.StepRequest.CellStateEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='agent.StepRequest.CellStateEntry.value', index=1,
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
  serialized_start=111,
  serialized_end=159,
)

_STEPREQUEST = _descriptor.Descriptor(
  name='StepRequest',
  full_name='agent.StepRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='numSteps', full_name='agent.StepRequest.numSteps', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cell_state', full_name='agent.StepRequest.cell_state', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_STEPREQUEST_CELLSTATEENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=23,
  serialized_end=159,
)


_STATERESPONSE_EMISSIONSENTRY = _descriptor.Descriptor(
  name='EmissionsEntry',
  full_name='agent.StateResponse.EmissionsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='agent.StateResponse.EmissionsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='agent.StateResponse.EmissionsEntry.value', index=1,
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
  serialized_start=256,
  serialized_end=304,
)

_STATERESPONSE = _descriptor.Descriptor(
  name='StateResponse',
  full_name='agent.StateResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='currentStep', full_name='agent.StateResponse.currentStep', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='emissions', full_name='agent.StateResponse.emissions', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_STATERESPONSE_EMISSIONSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=162,
  serialized_end=304,
)

_STEPREQUEST_CELLSTATEENTRY.containing_type = _STEPREQUEST
_STEPREQUEST.fields_by_name['cell_state'].message_type = _STEPREQUEST_CELLSTATEENTRY
_STATERESPONSE_EMISSIONSENTRY.containing_type = _STATERESPONSE
_STATERESPONSE.fields_by_name['emissions'].message_type = _STATERESPONSE_EMISSIONSENTRY
DESCRIPTOR.message_types_by_name['StepRequest'] = _STEPREQUEST
DESCRIPTOR.message_types_by_name['StateResponse'] = _STATERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

StepRequest = _reflection.GeneratedProtocolMessageType('StepRequest', (_message.Message,), {

  'CellStateEntry' : _reflection.GeneratedProtocolMessageType('CellStateEntry', (_message.Message,), {
    'DESCRIPTOR' : _STEPREQUEST_CELLSTATEENTRY,
    '__module__' : 'agent_pb2'
    # @@protoc_insertion_point(class_scope:agent.StepRequest.CellStateEntry)
    })
  ,
  'DESCRIPTOR' : _STEPREQUEST,
  '__module__' : 'agent_pb2'
  # @@protoc_insertion_point(class_scope:agent.StepRequest)
  })
_sym_db.RegisterMessage(StepRequest)
_sym_db.RegisterMessage(StepRequest.CellStateEntry)

StateResponse = _reflection.GeneratedProtocolMessageType('StateResponse', (_message.Message,), {

  'EmissionsEntry' : _reflection.GeneratedProtocolMessageType('EmissionsEntry', (_message.Message,), {
    'DESCRIPTOR' : _STATERESPONSE_EMISSIONSENTRY,
    '__module__' : 'agent_pb2'
    # @@protoc_insertion_point(class_scope:agent.StateResponse.EmissionsEntry)
    })
  ,
  'DESCRIPTOR' : _STATERESPONSE,
  '__module__' : 'agent_pb2'
  # @@protoc_insertion_point(class_scope:agent.StateResponse)
  })
_sym_db.RegisterMessage(StateResponse)
_sym_db.RegisterMessage(StateResponse.EmissionsEntry)


_STEPREQUEST_CELLSTATEENTRY._options = None
_STATERESPONSE_EMISSIONSENTRY._options = None

_AGENT = _descriptor.ServiceDescriptor(
  name='Agent',
  full_name='agent.Agent',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=306,
  serialized_end=369,
  methods=[
  _descriptor.MethodDescriptor(
    name='get_action',
    full_name='agent.Agent.get_action',
    index=0,
    containing_service=None,
    input_type=_STATERESPONSE,
    output_type=_STEPREQUEST,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_AGENT)

DESCRIPTOR.services_by_name['Agent'] = _AGENT

# @@protoc_insertion_point(module_scope)