import turtle

turtle.color('black')
turtle.speed('fast')

# Body
turtle.begin_fill()

turtle.lt(105)
turtle.fd(100)
xl,yl = turtle.pos()
lh = turtle.heading()
turtle.rt(105)
turtle.fd(55)
xr,yr = turtle.pos()
rh = turtle.heading()
turtle.rt(105)
turtle.fd(100)

turtle.end_fill()

x,y = turtle.pos()
turtle.width(3)

# Left leg
turtle.setpos(x/2,y/2)
turtle.seth(0)
turtle.rt(100)
turtle.fd(65)
turtle.lt(0)
turtle.fd(65)

# Right leg
turtle.up()
turtle.setpos(x/2,y/2)
turtle.lt(20)
turtle.down()

turtle.fd(65)
turtle.rt(0)
turtle.fd(65)

# Head
turtle.up()
turtle.setpos(0,98)
turtle.seth(0)
turtle.down()

turtle.circle(20)

# Left arm
turtle.up()
turtle.setpos(xl,yl)
turtle.seth(lh)
turtle.lt(45)
turtle.down()

turtle.fd(50)
turtle.rt(10)
turtle.fd(50)

# Right arm
turtle.up()
turtle.setpos(xr,yr)
turtle.seth(rh)
turtle.lt(30)
turtle.down()

turtle.fd(50)
turtle.lt(10)
turtle.fd(50)

# Wheel
turtle.up()
turtle.setpos(0,-130)
turtle.seth(0)
turtle.down()

turtle.circle(170)

# Wheel upper grip
turtle.up()
turtle.setpos(-30,205)
turtle.seth(-30)
turtle.down()

turtle.fd(20)
turtle.seth(0)
turtle.fd(30)
turtle.seth(30)
turtle.fd(20)

turtle.done()
