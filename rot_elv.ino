#include <AFMotor.h> //библиотека для управления шаговыми двигателями
unsigned long last_time; //число в диапазоне от нуля до 9 миллионов, хранится время
const int  stepsPerRevolution = 200;// константа, число шагов на один оборот движка
AF_Stepper elevation(stepsPerRevolution, 2); //создаем обьект движка элевации
AF_Stepper rotation(stepsPerRevolution, 1); //создаем объект движка азимута
//400 шагов равняется приблизительно 90 градусов, 1 шаг приблизительно равен 0.225 градусов
//аналоговые входов 5 штук, нумеруются от 14 до 19
const int buttonPin0 = 14;
const int buttonPin1 = 15;
const int buttonPin2 = 16;
const int buttonPin3 = 17;
const int concevicPin4 = 18;
const int concevicPin5 = 19;
void setup() {
  pinMode(buttonPin0, INPUT);
  pinMode(buttonPin1, INPUT);
  pinMode(buttonPin2, INPUT);
  pinMode(buttonPin3, INPUT);
  pinMode(concevicPin4, INPUT);
  pinMode(concevicPin5, INPUT);
  elevation.setSpeed(25);//количество оборотов в минуту
  rotation.setSpeed(5); //количество оборотов в минуту
  Serial.begin(9600);
  while(analogRead(concevicPin5)<300) elevation.step(2,FORWARD,SINGLE);// Выставляем ноль для элевации
  while(analogRead(concevicPin4)<300) rotation.step(2,BACKWARD,SINGLE);// Выставляем ноль для азимута

}
void loop() {
  if(analogRead(buttonPin0)>300 && analogRead(concevicPin5)<300){
    last_time=millis();
  while(analogRead(buttonPin0)>300){
    if(millis()-last_time>2000){
    elevation.setSpeed(100);
    }
    elevation.step(2, FORWARD, SINGLE);
    elevation.setSpeed(25);
  }
  }
  if(analogRead(buttonPin1)>300){
    last_time=millis();
  while(analogRead(buttonPin1)>300){
    if(millis()-last_time>2000){
    elevation.setSpeed(100);
    }
    elevation.step(2, BACKWARD, SINGLE);
    elevation.setSpeed(25);
  }
  }
  if(analogRead(buttonPin2)>300){
     last_time=millis();
    while(analogRead(buttonPin2)>300){
      if(millis()-last_time>2000){
        rotation.setSpeed(25);
        }
    rotation.step(2,FORWARD,SINGLE);
    rotation.setSpeed(5);
  }
  }
  if(analogRead(buttonPin3)>300 && analogRead(concevicPin4)<300){
    last_time=millis();
    while(analogRead(buttonPin3)>300){
      if(millis()-last_time>2000){
        rotation.setSpeed(25);
        }
    rotation.step(2,BACKWARD,SINGLE);
    rotation.setSpeed(5);
  }
  
}
}

//ВЕСЬ КОД ДАЛЬШЕ ДЛЯ УДОБСТВА
/*if(analogRead(buttonPin0)>300){
    last_time=millis();
  while(analogRead(buttonPin0)>300){
    if(millis()-last_time>2000){
    elevation.setSpeed(100);
    }
    elevation.step(2, FORWARD, SINGLE);
    elevation.setSpeed(25);
  }
  }
  if(analogRead(buttonPin1)>300){
    last_time=millis();
  while(analogRead(buttonPin1)>300){
    if(millis()-last_time>2000){
    elevation.setSpeed(100);
    }
    elevation.step(2, BACKWARD, SINGLE);
    elevation.setSpeed(25);
  }
  }
  if(analogRead(buttonPin2)>300){
     last_time=millis();
    while(analogRead(buttonPin2)>300){
      if(millis()-last_time>2000){
        rotation.setSpeed(25);
        }
    rotation.step(2,FORWARD,SINGLE);
    rotation.setSpeed(5);
  }
  }
  if(analogRead(buttonPin3)>300){
    last_time=millis();
    while(analogRead(buttonPin3)>300){
      if(millis()-last_time>2000){
        rotation.setSpeed(25);
        }
    rotation.step(2,BACKWARD,SINGLE);
    rotation.setSpeed(5);
  }
  }*/

/////////////////////////////////////
/////////////////////////////////////
  /*if(analogRead(buttonPin0)>300){
    elevation.step(2,FORWARD,SINGLE);
  }
  if(analogRead(buttonPin1)>300){
    elevation.step(2,BACKWARD,SINGLE);
  }
  if(analogRead(buttonPin2)>300){
    rotation.step(2,FORWARD,SINGLE);
  }
  if(analogRead(buttonPin3)>300){
    rotation.step(2,BACKWARD,SINGLE);
  }*/
