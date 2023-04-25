# 6DOF

## 1 Описание проекта

Данный проект создан для изучения возможностей [тренажёра](https://auto-sys.su/products/astm/) (зелёный), спроектированного на базе 6-ти степенной платформы Стюарта на угловых актуаторах.

![312683cc-cc83-4923-8dc0-b2953b33f5bf b5ASy](https://user-images.githubusercontent.com/86445241/231889804-f48c49f6-d8e7-466a-b50d-0ffda538c0c9.jpg)|![1  Graph, default position of platform](https://user-images.githubusercontent.com/86445241/231886267-50940a10-0ec4-424c-b39e-7f0f63999aef.png)
---|---
а). | б).  <br />

Рисунок 1 - тренажёр AST: а - тренажёр; б - схематичная визуализация результата расчёта (см. ветвь [visualization](https://github.com/LiDline/6DOF/tree/visualization)).

 Проект содержит 3 ветви:
1. main - реализация скрипта на python, возвращающего углы угловых актуаторов (редукторов) по заданным координатам и углам верхней платформы;
2. visualization - схематичная визуализация результата расчёта. Предварительный просмотр [тут](https://chart-studio.plotly.com/~LiDline/1.embed).
3. test - используемая в проекте теория по платформе.

## 2 Запуск программ
...

## 3 Состав ветки test
Ветка visualization является продолжением ветки main (т.е. файлы ветки изменены для дополнения return).
- папка func - содержит в себе необходимые функции для...
1. Plane.ipynb - блокнот с объяснением реализации матрицы поворота на примере пластины. Аналогичная информация представлена [тут](https://hedgedoc.auto-sys.su/JAqGGd3JRn-qmUJVMdjODg).
2. Sphere&circle.ipynb - блокнот со способом нахождения точки пересечения рычага редуктора и тяги верхней плиты. Аналогичная информация представлена [тут](https://hedgedoc.auto-sys.su/JAqGGd3JRn-qmUJVMdjODg).

## 4 Используемые библиотеки
- numpy;
- plotly;
- datetime;
- файлы блокнота Jupiter.
____
Все используемые библиотеки python указаны в файле requirements.txt. Для быстрой установки отсутствующих библиотек в терминале выполните: 
```
pip install -r requirements.txt
```