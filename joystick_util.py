from gpiozero import Button

up = Button(6)
left = Button(17)
down = Button(23)
right = Button(18)
enter = Button(22)

if __name__ == "__main__":
    
    up.when_pressed = lambda x: print("up")