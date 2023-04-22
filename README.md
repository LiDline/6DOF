# 6DOF

## 1 Описание проекта

Данный проект создан для изучения возможностей [тренажёра](https://auto-sys.su/products/astm/) (зелёный), спроектированного на базе 6-ти степенной платформы Стюарта на угловых актуаторах.

![312683cc-cc83-4923-8dc0-b2953b33f5bf b5ASy](https://user-images.githubusercontent.com/86445241/231889804-f48c49f6-d8e7-466a-b50d-0ffda538c0c9.jpg)|![1  Graph, default position of platform](https://user-images.githubusercontent.com/86445241/231886267-50940a10-0ec4-424c-b39e-7f0f63999aef.png)
---|---
а). | б).  <br />

Рисунок 1 - тренажёр AST: а - тренажёр; б - схематичная визуализация результата расчёта (см. ветвь [visualization](https://github.com/LiDline/6DOF/tree/visualization)).

 Проект содержит 3 ветви:
1. main - реализация скрипта на python, возвращающего углы угловых актуаторов (редукторов) по заданным координатам и углам верхней платформы;
2. visualization - схематичная визуализация результата расчёта;
3. test - используемая в проекте теория по платформе.

## 2 Запуск программы
Ветка visualization является продолжением ветки main (т.е. файлы ветки изменены для дополнения return).
```python
python3 visualization.py
```

Если заданные на входе параметры приведут к выходу за диапазон работы платформы, Вам вернут сообщение об этом (будет конкретно написано, какая часть платформы сломана). 

Допустимые диапазоны характеристик (находятся в constants.py):
- max угол шаровых = 35 град;
- min/max длина пружины (от шаровой до шаровой) = [464, 714] мм;
- max/min угол актуаторов = [-112.38, 52.62] град.

## 3 Состав ветки visualization
1. папка func - содержит в себе необходимые функции для математического расчёта платформы. Состав дополнен следующими файлами:
- added_first_number.py - скрипт для преобразования координат для plotly;
- coordinate_system.py - вычисление координат отрисовываемых СК;
- Graph.py - класс отрисовки графика.
2. папка SW - файлы SolidWorks 2020 со схемой платформы (состава аналогичен ветки main).
3. constants.py - файл с изменяемыми константами платформы.
4. main.py - файл с функцией расчёта платформы.
5. visualization.py - исполняемый файл.

## 4 Используемые библиотеки
- numpy;
- plotly.
____
Все используемые библиотеки python указаны в файле requirements.txt. Для быстрой установки отсутствующих библиотек в терминале выполните: 
```
pip install -r requirements.txt
```
## 5 Вариации использования скрипта

1. Изменить координаты точек крепления шаровых редукторов/пружин можно в матрицах в файле constants.py со строки 22.
2. Изменить допустимые диапазоны характеристик можно в файле constants.py со строки 11.

## 6 Проверка значений

1. Проверку полученных углов можно совершить в SW/AST-5.2.0-A1-scetch.SLDASM. Sketch "***Рычаг[i+1]***" = углу актуатора. На рисунке 2, а мы видим, что угол равен 55.88 град, что совпадает с solve(25, 25, 300, 5, 5, 5)[0] (знаки углов разные, см. пункт 6). 
2. В Sketch "***Угол шаровой[i+1]-1*** или ***2***" можно увидеть угол шаровой опоры.

![Проверка угла 0](https://user-images.githubusercontent.com/86445241/231896653-c5e6d8c8-8337-4123-a9c6-0ce3dfde19ac.png)|![Изменение положения](https://user-images.githubusercontent.com/86445241/231896717-9eafa52d-ff11-416e-bddb-7d6951c053db.png)
---|---
a).|б). <br />

Рисунок 2 - схема тренажера: а - угол нулевого актуатора = 55.88 град; б - способ изменения параметров. 

## 7 Определение углов
Введём локальную систему координат (далее СК) для определения углов. За ось поворота принимаем OZ (как в Matlab Simscape Multibody.  синяя линия рисунке 3, а). Ось OY (зелёная линия на рисунке 3, а) направлена на противоположную плиту. Ось OX (красная линия на рисунке 3, а) направлена на OX редуктора, расположенного в одной плоскости. <br />

### 7.1 Определение угла редуктора

Угол редуктора вычисляем относительно OY (рисунок 3, б). Важно отметить, что **в SW отрицательных углов нет**, в скрипте угол вычисляется через atan2: в I четверти знак положительный, во второй => отрицательный. Мы выбираем НАИМЕНЬШИЙ угол, который вписывается в диапазон max/min углов редукторов = [-112.38, 52.62] град (это конструкционные ограничения). <br />
См. подробный разбор нахождения углов [тут](https://hedgedoc.auto-sys.su/JAqGGd3JRn-qmUJVMdjODg) или [тут] в файле (https://github.com/LiDline/6DOF/tree/test) "**2. Sphere&circle.ipynb**".

![1](https://user-images.githubusercontent.com/86445241/232336460-858e7131-d233-469b-af6a-b62f14796a9e.png)|![2](https://user-images.githubusercontent.com/86445241/232336490-214af603-e1a8-474a-a9f0-af731c765a3b.png)
---|---
a).|б). <br />

Рисунок 2 - Определение угла редуктора: а - локальные СК для плит; б - определение угла редуктора в локальных СК.

### 7.2 Определение угла шаровой опоры

Для определения угла шаровой опоры на рычаге редуктора (файл leg_ball_corners.py) необходимо:

1. Найти координаты точки пересечения (см. рисунок 3, а) окружности (рычага редуктора) и сферы (тяги) и записать её в матричном виде.
2. Определим координаты верхней шаровой опоры тяги относительно точки пересечения путём перемножения обратной матрицы перемещений точки пересечения и матрицы координат верхней точки (строка 78).
3. Найдём угол между проекцией тяги (на локальной XY) и верхней точки (см. рисунок 3, б), чтобы повернуть локальную СК на полученный угол (строка 82). Создадим матрицу поворота из полученного угла и домножим её на матрицу из пункта 2 (строка 88).
4. Узнаем координаты верхней шаровой опоры тяги относительно точки пересечения в полученной СК путём перемножения обратной матрицы из пункта 3. на матрицу координат верхней точки (строка 97).
5. Находим угол (рисунок 3, в) через вычисление math.atan2(X, Z), где X и Z - координаты верхней точки из пункта 4 (строка 102).