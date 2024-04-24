from gui import Display


display = Display()


def action(x: int, y: int):
    print(x,y)

display.bind_function(action)










if __name__ == '__main__':
    display.mainloop()



    ...




