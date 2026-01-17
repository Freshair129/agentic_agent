"Complexity"

Module + Module = System,Sub System
Module + System = System
System + System = System,Core System

Sub System ไม่มีสิท pub/sub ใน bus

Node + Node = Module
node + module = system,sub system
module + module = system,sub system

กรณีนี้ node + module อาจจะงงว่าทำไม ไม่รวม node เข้าไปใน module เลย
แสดงว่า node ไม่มีสิทธิ์ในการสื่อสารกับ node ตัวอื่น หรือ อาจจะเป็น Central Node หรือเป็น enginge (ซึ่งไม่แน่ใจว่ามันซ้ำกับtoolsไหม)

Sub System ไม่มีสิทธิ์ในการสื่อสารกับ System ตัวอื่นนอกจาก owner ของมันเอง
เช่น RMS  นี้มี 1 โมดูล(trauma store) ทำงานคู่กับ 1 system ระบบทาสีความทรงจำ โดยมี MSP เป็นเจ้าของ แต่เพื่อไม่ให้ MSP load เยอะเกินจึงสร้าง RMS มาดูเเล ซึ่งมันซับซ้อนเกินกว่าที่จะเป็นโมดูลและก็ไม่ได้สื่อสารกับ System ตัวอื่นนอกจาก MSP และไม่จำเป็นต้องสื่อสารกับ ฺBUS เพราะ MSPต้องการแค่ผลลัพแล้วติดต่อกับ BUSเอง
