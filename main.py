import model


if __name__ == "__main__":
    m = model.Model()
    print(m)
    for i in range(len(m.space.bodies)):
        print(m.space.bodies[i], m.space.bodies[i].position)
    for _ in range(200):
        m.step()
        for i in range(len(m.space.bodies)):
            print(m.space.bodies[i], m.space.bodies[i].position)
