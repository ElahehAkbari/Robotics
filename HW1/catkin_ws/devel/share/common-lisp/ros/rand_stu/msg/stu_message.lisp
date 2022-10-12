; Auto-generated. Do not edit!


(cl:in-package rand_stu-msg)


;//! \htmlinclude stu_message.msg.html

(cl:defclass <stu_message> (roslisp-msg-protocol:ros-message)
  ((name
    :reader name
    :initarg :name
    :type cl:string
    :initform "")
   (age
    :reader age
    :initarg :age
    :type cl:fixnum
    :initform 0)
   (last_name
    :reader last_name
    :initarg :last_name
    :type cl:string
    :initform "")
   (department
    :reader department
    :initarg :department
    :type cl:string
    :initform ""))
)

(cl:defclass stu_message (<stu_message>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <stu_message>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'stu_message)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name rand_stu-msg:<stu_message> is deprecated: use rand_stu-msg:stu_message instead.")))

(cl:ensure-generic-function 'name-val :lambda-list '(m))
(cl:defmethod name-val ((m <stu_message>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rand_stu-msg:name-val is deprecated.  Use rand_stu-msg:name instead.")
  (name m))

(cl:ensure-generic-function 'age-val :lambda-list '(m))
(cl:defmethod age-val ((m <stu_message>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rand_stu-msg:age-val is deprecated.  Use rand_stu-msg:age instead.")
  (age m))

(cl:ensure-generic-function 'last_name-val :lambda-list '(m))
(cl:defmethod last_name-val ((m <stu_message>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rand_stu-msg:last_name-val is deprecated.  Use rand_stu-msg:last_name instead.")
  (last_name m))

(cl:ensure-generic-function 'department-val :lambda-list '(m))
(cl:defmethod department-val ((m <stu_message>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rand_stu-msg:department-val is deprecated.  Use rand_stu-msg:department instead.")
  (department m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <stu_message>) ostream)
  "Serializes a message object of type '<stu_message>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'name))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'name))
  (cl:let* ((signed (cl:slot-value msg 'age)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'last_name))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'last_name))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'department))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'department))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <stu_message>) istream)
  "Deserializes a message object of type '<stu_message>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'name) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'name) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'age) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'last_name) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'last_name) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'department) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'department) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<stu_message>)))
  "Returns string type for a message object of type '<stu_message>"
  "rand_stu/stu_message")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'stu_message)))
  "Returns string type for a message object of type 'stu_message"
  "rand_stu/stu_message")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<stu_message>)))
  "Returns md5sum for a message object of type '<stu_message>"
  "64bbd1451ffce53d77c080a112ddaa04")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'stu_message)))
  "Returns md5sum for a message object of type 'stu_message"
  "64bbd1451ffce53d77c080a112ddaa04")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<stu_message>)))
  "Returns full string definition for message of type '<stu_message>"
  (cl:format cl:nil "string name~%int8 age~%string last_name~%string department~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'stu_message)))
  "Returns full string definition for message of type 'stu_message"
  (cl:format cl:nil "string name~%int8 age~%string last_name~%string department~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <stu_message>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'name))
     1
     4 (cl:length (cl:slot-value msg 'last_name))
     4 (cl:length (cl:slot-value msg 'department))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <stu_message>))
  "Converts a ROS message object to a list"
  (cl:list 'stu_message
    (cl:cons ':name (name msg))
    (cl:cons ':age (age msg))
    (cl:cons ':last_name (last_name msg))
    (cl:cons ':department (department msg))
))
