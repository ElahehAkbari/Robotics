;; Auto-generated. Do not edit!


(when (boundp 'rand_stu::stu_message)
  (if (not (find-package "RAND_STU"))
    (make-package "RAND_STU"))
  (shadow 'stu_message (find-package "RAND_STU")))
(unless (find-package "RAND_STU::STU_MESSAGE")
  (make-package "RAND_STU::STU_MESSAGE"))

(in-package "ROS")
;;//! \htmlinclude stu_message.msg.html


(defclass rand_stu::stu_message
  :super ros::object
  :slots (_name _age _last_name _department ))

(defmethod rand_stu::stu_message
  (:init
   (&key
    ((:name __name) "")
    ((:age __age) 0)
    ((:last_name __last_name) "")
    ((:department __department) "")
    )
   (send-super :init)
   (setq _name (string __name))
   (setq _age (round __age))
   (setq _last_name (string __last_name))
   (setq _department (string __department))
   self)
  (:name
   (&optional __name)
   (if __name (setq _name __name)) _name)
  (:age
   (&optional __age)
   (if __age (setq _age __age)) _age)
  (:last_name
   (&optional __last_name)
   (if __last_name (setq _last_name __last_name)) _last_name)
  (:department
   (&optional __department)
   (if __department (setq _department __department)) _department)
  (:serialization-length
   ()
   (+
    ;; string _name
    4 (length _name)
    ;; int8 _age
    1
    ;; string _last_name
    4 (length _last_name)
    ;; string _department
    4 (length _department)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _name
       (write-long (length _name) s) (princ _name s)
     ;; int8 _age
       (write-byte _age s)
     ;; string _last_name
       (write-long (length _last_name) s) (princ _last_name s)
     ;; string _department
       (write-long (length _department) s) (princ _department s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _name
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _name (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; int8 _age
     (setq _age (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _age 127) (setq _age (- _age 256)))
   ;; string _last_name
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _last_name (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _department
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _department (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(setf (get rand_stu::stu_message :md5sum-) "64bbd1451ffce53d77c080a112ddaa04")
(setf (get rand_stu::stu_message :datatype-) "rand_stu/stu_message")
(setf (get rand_stu::stu_message :definition-)
      "string name
int8 age
string last_name
string department

")



(provide :rand_stu/stu_message "64bbd1451ffce53d77c080a112ddaa04")


