# 6DOF

## 1 Описание проекта

Данный проект создан для изучения возможностей [тренажёра](https://auto-sys.su/products/astm/) (зелёный), спроектированного на базе 6-ти степенной платформы Стюрта на угловых актуаторах.

![312683cc-cc83-4923-8dc0-b2953b33f5bf b5ASy](https://user-images.githubusercontent.com/86445241/231889804-f48c49f6-d8e7-466a-b50d-0ffda538c0c9.jpg)|![1  Graph, default position of platform](https://user-images.githubusercontent.com/86445241/231886267-50940a10-0ec4-424c-b39e-7f0f63999aef.png)
---|---
а). | б).  <br />

Рисунок 1 - тренажёр AST: а - 3D-модель; б - схематичная визуализация результата расчёта (см. ветвь [visualization](https://github.com/LiDline/6DOF/tree/visualization)).

 Проект содержит 3 ветви:
1. main - реализация скрипта на python, возвращающего углы угловых актуаторов (редукторов) по заданным координатам и углам верхней платформы;
2. visualization - схематичная визуализация результата расчёта;
3. test - используемая в проекте теория по платформе.

## 2 Работа скрипта
arms_degrees_with_angular_limit_on_joint_and_arm.py несёт в себе фунцию:
```python
def solve(x, y, z, alpha, beta, gamma): # Example: (25, 25, 300, 5, 5, 5)
```
На вход подаётся 6 параметров:
- x - координата X (мм);
- y - координата Y (мм);
- z - координата Z (мм);
- alpha - угол OX (градусы);
- beta - угол OY (градусы);
- gamma - угол OZ (градусы). <br />

Результатом работы функции будет список из 6-ти НАИМЕНЬШИХ углов (относительно вертикальной оси OZ. OZ = 0 град) редукторов:
```python
return arm_angle # Example: [-55.88 -54.72 -92.84 -54.10 -58.97 -50.18] перевёл в градусы для удобства*
# На рисунке 2, а приведено значение угла для solve(25, 25, 300, 5, 5, 5)[0] = 55.89 град.
```
Если заданные на входе параметры приведут к выходу за диапазон работы платформы, Вам вернут сообщение об этом (будет конкретно написано, какая часть платформы сломана). 

## 3 Состав ветки main
1. папка func - содержит в себе необходимые функции:
- cross_normal_to_oz.py - точки пересечение между окружностью (редуктором) и сферой (тяга). См. подробный разбор [тут](https://hedgedoc.auto-sys.su/JAqGGd3JRn-qmUJVMdjODg);
- matrix_1_4.py - запись получаемых координат XYZ (из cross_normal_to_oz.py) в ортогональных координатах (добавляем 1 в конец списка);
- rotation_matrix.py - реализация матрицы поворота по последовательности XYZ и запись её в ортогональных координатах (матрица 4х4);
- transition_matrix.py - матрица линейного переноса координат (матрица 4х4) - cюда записываем НА сколько перемещаемся;
2. папка SW - файлы SolidWorks 2020 со схемой(AST-5.2.0-A1-scetch.SLDASM) платформы для проверки (см. рисунок 1, а) получаемых углов шаровых опор актуаторов и уравновешивающих механизмов (менять углы/координаты верхней плиты необходимо через управляемые сопряжения, см. рисунок 1, б).

3. arms_degrees_with_angular_limit_on_joint_and_arm.py - исполнительный файл.

## 3 Используемые библиотеки
...
____
Все используемые библиотеки python указаны в файле requirements.txt. Для быстрой установки отсутствующих библиотек в терминале выполните: 
```
pip install -r requirements.txt
```
## 4 Варации использования скрипта и проверка

1. Измененить координаты точек крепления шаровых редукторов/пружин можно в матрицах со строки 22.
2. Проверку полученных углов можно совершить в SW/AST-5.2.0-A1-scetch.SLDASM. Sketch "***Рычаг[i+1]***" = углу актуатора. На рисунке 2, а мы видим, что угол равен 55.88 град (что совпадает с solve(25, 25, 300, 5, 5, 5)[0] - в SW отрицательных углов нет). 
3. В Sketch "***Угол шаровой[i+1]-1*** или ***2***" можно увидеть угол шаровой опоры.

![Проверка угла 0](https://user-images.githubusercontent.com/86445241/231896653-c5e6d8c8-8337-4123-a9c6-0ce3dfde19ac.png)|![Изменение положения](https://user-images.githubusercontent.com/86445241/231896717-9eafa52d-ff11-416e-bddb-7d6951c053db.png)
---|---
a).|б). <br />

Рисунок 2 - схема тренажера: а - угол нулевого актуатора = 55.88 град; б - способ изменения параметров. 