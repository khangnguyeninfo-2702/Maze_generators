class Button:
    def __init__(self, image, text_input, pos, font, base_color, hovering_color):
        white = (255, 255, 255)
        self.image, self.text_input = image, text_input
        self.x_cor = pos[0]
        self.y_cor = pos[1]
        self.font, self.base_color, self.hovering_color = font, base_color, hovering_color
        self.text = self.font.render(self.text_input, True, white)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_cor, self.y_cor))
        self.text_rect = self.text.get_rect(center=(self.x_cor, self.y_cor))

    # Present the image/ texts on screen.
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    # Check if the position in the input is colliding with the button.
    def checkforInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    # Changes the button color if (position) is hovering over it.
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

    # Get the size of the button
    def get_size(self):
        return self.rect.size