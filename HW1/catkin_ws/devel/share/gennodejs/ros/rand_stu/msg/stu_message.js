// Auto-generated. Do not edit!

// (in-package rand_stu.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class stu_message {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.name = null;
      this.age = null;
      this.last_name = null;
      this.department = null;
    }
    else {
      if (initObj.hasOwnProperty('name')) {
        this.name = initObj.name
      }
      else {
        this.name = '';
      }
      if (initObj.hasOwnProperty('age')) {
        this.age = initObj.age
      }
      else {
        this.age = 0;
      }
      if (initObj.hasOwnProperty('last_name')) {
        this.last_name = initObj.last_name
      }
      else {
        this.last_name = '';
      }
      if (initObj.hasOwnProperty('department')) {
        this.department = initObj.department
      }
      else {
        this.department = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type stu_message
    // Serialize message field [name]
    bufferOffset = _serializer.string(obj.name, buffer, bufferOffset);
    // Serialize message field [age]
    bufferOffset = _serializer.int8(obj.age, buffer, bufferOffset);
    // Serialize message field [last_name]
    bufferOffset = _serializer.string(obj.last_name, buffer, bufferOffset);
    // Serialize message field [department]
    bufferOffset = _serializer.string(obj.department, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type stu_message
    let len;
    let data = new stu_message(null);
    // Deserialize message field [name]
    data.name = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [age]
    data.age = _deserializer.int8(buffer, bufferOffset);
    // Deserialize message field [last_name]
    data.last_name = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [department]
    data.department = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.name);
    length += _getByteLength(object.last_name);
    length += _getByteLength(object.department);
    return length + 13;
  }

  static datatype() {
    // Returns string type for a message object
    return 'rand_stu/stu_message';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '64bbd1451ffce53d77c080a112ddaa04';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string name
    int8 age
    string last_name
    string department
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new stu_message(null);
    if (msg.name !== undefined) {
      resolved.name = msg.name;
    }
    else {
      resolved.name = ''
    }

    if (msg.age !== undefined) {
      resolved.age = msg.age;
    }
    else {
      resolved.age = 0
    }

    if (msg.last_name !== undefined) {
      resolved.last_name = msg.last_name;
    }
    else {
      resolved.last_name = ''
    }

    if (msg.department !== undefined) {
      resolved.department = msg.department;
    }
    else {
      resolved.department = ''
    }

    return resolved;
    }
};

module.exports = stu_message;
