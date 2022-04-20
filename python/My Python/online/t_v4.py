import turtle
t = turtle.Turtle()
t.shape('turtle')

while True:
    command = input("빨간 삼각형 'o', 노란원은 'p', 종료는 'q'를 입력하세요: ")

    if command == 'o':
        t.color('red')
        t.begin_fill()
        for i in range(3):
            t.forward(130)
            t.left(120)
        t.end_fill()

    if command == 'p':
           t.color('yellow')
           t.begin_fill()
           t.circle(100)
           t.end_fill()

    if command == 'q':
            break
