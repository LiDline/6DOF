# 6DOF

## 1 Описание проекта

Данный проект создан для изучения возможностей [тренажёра](https://auto-sys.su/products/astm/) (зелёный), спроектированного на базе 6-ти степенной платформы Стюрта на угловых актуаторах. Проект содержит 2 ветви:
1. main - реализация скрипта на python, возвращающего углы угловых актуаторов (редукторов) по заданным координатам и углам верхней платформы.
2. ...

## 2 Запуск программы
Запуск скрипта осуществляется через:
```
python3 arms_degrees_with_angular_limit_on_joint_and_arm.py
```
На вход подаётся 6 параметров:
- координата X (мм);
- координата Y (мм);
- координата Z (мм);
- угол aX (градусы);
- угол Ay (градусы);
- угол Az (градусы).
<br />
Результатом работы скрипта будет список из 6-ти углов редукторов (радианы). Если заданные на входе параметры приведут к выходу за диапазон работы платформы, Вам вернут сообщение об этом (будет конкретно написано, какая часть платформы сломана). 

## 3 Состав ветки main
1. папка func - содержит в себе необходимые функции:
- cross_normal_to_oz.py - точки пересечение между окружностью (редуктором) и сферой (тяга). См. подробный разбор [тут](https://hedgedoc.auto-sys.su/JAqGGd3JRn-qmUJVMdjODg);
- matrix_1_4.py - запись получаемых координат XYZ (из cross_normal_to_oz.py) в ортогональных координатах (добавляем 1 в конец списка);
- rotation_matrix.py - реализация матрицы поворота по последовательности XYZ и запись её в ортогональных координатах (матрица 4х4);
- transition_matrix.py - матрица линейного переноса координат (матрица 4х4) - cюда записываем НА сколько перемещаемся;
2. папка SW - файлы SolidWorks 2020 со схемой(AST-5.2.0-A1-scetch.SLDASM) платформы для проверки получаемых углов шаровых опор актуаторов и уравновешивающих механизмов (менять углы/координаты верхней плиты необходимо через управляемые сопряжения).
3. arms_degrees_with_angular_limit_on_joint_and_arm.py - исполнительный файл.

## 3 Используемые библиотеки
...
____
Все используемые библиотеки python указаны в файле requirements.txt. Для быстрой установки отсутствующих библиотек в терминале выполните: 
```
pip install -r requirements.txt
```
## 4 P.s.

1. Измененить координаты точек крепления шаровых редукторов/пружин можно в матрицах со строки 22.