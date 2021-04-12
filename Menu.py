import arcade
import arcade.gui
from typing import Optional
from uuid import uuid4
from arcade.gui import UIFlatButton, UIManager, UIClickable, UIImageButton
from arcade.gui.ui_style import UIStyle
from arcade.gui.utils import render_text_image
import random
import time


hori = 1280
vert = 720
titu = "The History Clicker"


class Entidade(arcade.Sprite):
    def __init__(self, x, y, arquivo, vida = 100, dano = 2):
        super().__init__(arquivo, center_x=x, center_y=y)
        self.vida = vida
        self.dano = dano
        self.vida_maxima = vida


class Vilao(Entidade):
    def __init__(self, x, y, arquivo, vida = random.randint(30, 40), dano = random.randint(20, 25)):
        super().__init__(x, y, arquivo, vida, dano)
        self.arq_moedas = open("Extras/Saves/Savemoeda.txt", "r")
        self.qtd_de_moedas = int(self.arq_moedas.read())
        self.arq_moedas.close()
        self.brilho = False
        self.lista_monstros = ["Extras/Imagens/Monster0.png", "Extras/Imagens/Monster1.png", "Extras/Imagens/Monster2.png", "Extras/Imagens/Monster3.png"]
        self.lista_monstros_mortos = ["Extras/Imagens/Monster0_Morto.png", "Extras/Imagens/Monster1_Morto.png", "Extras/Imagens/Monster2_Morto.png", "Extras/Imagens/Monster3_Morto.png"]
        self.lista_boss = ["Extras/Imagens/Boss0.png", "Extras/Imagens/Boss1.png"]
        self.lista_boss_mortos = ["Extras/Imagens/Boss0_Morto.png", "Extras/Imagens/Boss1_Morto.png"]

        self.lista_monstros_morrendo = ["Extras/Imagens/Monster0_Morrendo.png", "Extras/Imagens/Monster1_Morrendo.png", "Extras/Imagens/Monster2_Morrendo.png", "Extras/Imagens/Monster3_Morrendo.png"]
        self.lista_boss_morrendo = ["Extras/Imagens/Boss0_Morto.png", "Extras/Imagens/Boss1_Morrendo.png"]

        timer = -1
        self.arquivo = arquivo
        for i in self.lista_monstros:
            timer += 1
            if i == self.arquivo:
                self.monstro = i
                self.monstro_morto = self.lista_monstros_mortos[timer]
                self.monstro_morrendo = self.lista_monstros_morrendo[timer]
                timer = -1
        if self.arquivo == self.lista_boss[0]:
            self.monstro = self.arquivo
            self.monstro_morto = self.lista_boss_mortos[0]
            self.monstro_morrendo = self.lista_boss_morrendo[0]
        if self.arquivo == self.lista_boss[1]:
            self.monstro = self.arquivo
            self.monstro_morto = self.lista_boss_mortos[1]
            self.monstro_morrendo = self.lista_boss_morrendo[1]
        
        self.textures = [arcade.load_texture(self.monstro),  arcade.load_texture(self.monstro_morto)]
        self.current_texture = 0
        self.timer = 0
        
    def on_update(self, delta_time):      
        
        if self.vida <= 0:
            self.timer += delta_time
            self.textures = [arcade.load_texture(self.monstro),  arcade.load_texture(self.monstro_morrendo)]
            self.current_texture = 1 
            self.set_texture(self.current_texture)
            if self.timer >= 1.6:
                self.textures = [arcade.load_texture(self.monstro_morrendo),  arcade.load_texture(self.monstro_morto)]
                self.current_texture = 1 
                self.set_texture(self.current_texture)

            if self.timer >= 3.4:
                vilao_derrotado = open("Extras/Saves/Vilaoderrotado.txt", "r")
                self.qtd_derrotas = int(vilao_derrotado.read())
                vilao_derrotado.close()
                vilao_derrotado = open("Extras/Saves/Vilaoderrotado.txt", "w")
                vilao_derrotado.write(str(self.qtd_derrotas + 1))
                vilao_derrotado.close()
                save_moedas = open("Extras/Saves/Savemoeda.txt", "r")
                moedas = int(save_moedas.read())
                save_moedas.close()
                arq_moedas = open("Extras/Saves/Savemoeda.txt", "w")
                arq_moedas.write(str(moedas+75))
                arq_moedas.close()
                self.kill()
                return True


class Personagem(Entidade):
    def __init__(self, x, y, arquivo, vida = 100, dano = 4):
        super().__init__(x, y, arquivo, vida, dano)
        self.arq_cliques = open("Extras/Saves/Savecliques.txt", "r")
        self.qtd_de_clicks = int(self.arq_cliques.read())
        self.arq_cliques.close()

    def on_mouse_press(self, x, y, symbol, modifiers):
        if symbol == arcade.MOUSE_BUTTON_RIGHT:
            if x <= 1075 and x >= 780 and y >= 180 and y <= 650:
                self.qtd_de_clicks += 1
        if symbol == arcade.MOUSE_BUTTON_LEFT:
            if x <= 1075 and x >= 780 and y >= 180 and y <= 650:
                self.qtd_de_clicks += 1


class Menu_Principal(arcade.View):
    def __init__(self):
        super().__init__()
    
        self.ui_Manager = UIManager()
        self.setup()

    def on_draw(self):
        arcade.start_render()
        self.background = arcade.load_texture("Extras/Imagens/Background1.png")
        arcade.set_background_color(arcade.color.WHITE)
        arcade.draw_lrwh_rectangle_textured(0, 0, 1280, 720, self.background)

    def setup(self):
        botao_jogar = Botao_Jogar(self, Jogo(), "INICIAR JOGO", hori//2, vert//2+60, 320, 75, id=None)
        self.ui_Manager.add_ui_element(botao_jogar)
        botao_sair = Botao_sair("SAIR", hori//2, vert//2-60, 320, 75, id=None)
        self.ui_Manager.add_ui_element(botao_sair)
        texture = arcade.load_texture("Extras/Imagens/BotaoHelp.png")
        texturehover = arcade.load_texture("Extras/Imagens/BotaoHelpHover.png")
        texturepress = arcade.load_texture("Extras/Imagens/BotaoHelpHover.png")
        botao_help = Botao_MenuPrincipal(self, Menu_Ajuda(), 32, 687, texture, texturehover, texturepress)
        self.ui_Manager.add_ui_element(botao_help)
 
    def on_hide_view(self):
        self.ui_Manager.unregister_handlers()


class Menu_Ajuda(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_Manager = UIManager()
        
    def on_show_view(self):
        self.setup()
        

    def on_draw(self):
        arcade.start_render()
        self.background = arcade.load_texture("Extras/Imagens/Background4.png")
        arcade.draw_lrwh_rectangle_textured(0, 0, 1280, 720, self.background)

    def setup(self):
        botao_jogar = Botao_Jogar(self, Jogo(), "INICIAR JOGO", 1100, 185, 320, 75, id=None)
        self.ui_Manager.add_ui_element(botao_jogar)
        botao_sair = Botao_sair("SAIR", 1100, 75, 320, 75, id=None)
        self.ui_Manager.add_ui_element(botao_sair)

    def on_hide_view(self):
        self.ui_Manager.unregister_handlers()


class Jogo(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_Manager = UIManager()
        self.vilao = None
        self.personagem = None
        self.timer = 0
        self.lista_personagem = None
        self.vida_min = 75
        self.vida_max = 98
        self.dano_min = 2
        self.dano_max = 3
        self.timer1 = 0
        self.timer2 = 0
        self.vilao_morto = False
        self.lista_monstros = ["Extras/Imagens/Monster0.png", "Extras/Imagens/Monster1.png", "Extras/Imagens/Monster2.png", "Extras/Imagens/Monster3.png"]
        self.lista_boss = ["Extras/Imagens/Boss0.png", "Extras/Imagens/Boss1.png"]

    def on_update(self, delta_time):
        self.timer += delta_time
        self.timer2 += delta_time
        if self.timer2 >= 0.3:
            self.vilao.brilho = False
            self.timer2 = 0
        for elemento in self.lista_personagem:
            morto = elemento.on_update(delta_time)
            if morto:
                self.vilao_morto = True
          
        if self.vilao_morto == True:
            
            self.botao.set_vilao_morto()
            self.timer1 += delta_time
            if self.timer1 >= 2:
                boss = random.randint(1, 6)
                if boss == 5: 
                    self.vilao = Vilao(900, 400, self.lista_boss[random.randint(0, 1)], random.randint(self.vida_min*3, self.vida_max*3), random.randint(self.dano_min*3, self.dano_max*3))
                    self.botao.set_vilao_morto()
                else:
                    self.vilao = Vilao(900, 400, self.lista_monstros[random.randint(0, 3)], random.randint(self.vida_min, self.vida_max), random.randint(self.dano_min, self.dano_max))
                    self.botao.set_vilao_morto()

                self.lista_personagem.append(self.vilao)
                self.timer1 = 0
                self.vilao_morto = False
                self.vida_min *= 2
                self.vida_max *= 2
                self.dano_min *= 2
                self.dano_max *= 2

                    
        if self.timer >= random.randint(3, 8):
            self.personagem.vida -= self.vilao.dano
            self.timer = 0
            if self.personagem.vida <= 0:
                self.personagem.vida = 0
                Jogo().window.show_view(Gameover())

        arq = open("Extras/Saves/Vilaoderrotado.txt")
        self.vilao_derrotado = arq.read()
        arq.close()  

    def on_show_view(self):
        self.setup()

    def on_draw(self):
        arcade.start_render()
        self.background = arcade.load_texture("Extras/Imagens/Background2.png")
        arcade.draw_lrwh_rectangle_textured(0, 0, 1280, 720, self.background)
        if self.personagem is not None:
            cliques = str(self.personagem.qtd_de_clicks)
            moedas = str(self.vilao.qtd_de_moedas)
            self.lista_personagem.draw()

            arcade.draw_rectangle_filled(325, 640, 250*(self.personagem.vida/self.personagem.vida_maxima), 36, arcade.color.RED)
            arcade.draw_lrtb_rectangle_outline(200, 450, 658, 622, arcade.color.BLACK, 2)

            arcade.draw_rectangle_filled(900, 640, 250*(self.vilao.vida/self.vilao.vida_maxima), 36, arcade.color.RED)
            arcade.draw_lrtb_rectangle_outline(775, 1025, 658, 622, arcade.color.BLACK, 2)

        arcade.draw_text(cliques, 38, 700, arcade.color.WHITE, font_size=13)
        arcade.draw_text(moedas, 38, 672, arcade.color.WHITE, font_size=13)
        arcade.draw_text(str(self.vilao_derrotado), 38, 644, arcade.color.WHITE, font_size=13)
        cursor = arcade.load_texture("Extras/Imagens/Cursor.png")
        moeda = arcade.load_texture("Extras/Imagens/Moeda.png")
        morto = arcade.load_texture("Extras/Imagens/Monster2_Morto.png")
        arcade.draw_texture_rectangle(15, 680, 26, 26, moeda)
        arcade.draw_texture_rectangle(20, 705, 30, 30, cursor)
        arcade.draw_texture_rectangle(15, 655, 26, 26, morto)
        

    def on_mouse_press(self, x, y, symbol, modifiers):
        self.personagem.on_mouse_press(x, y, symbol, modifiers)   
        if symbol == arcade.MOUSE_BUTTON_LEFT or symbol == arcade.MOUSE_BUTTON_RIGHT:
            if x <= 1075 and x >= 780 and y >= 180 and y <= 650:
                self.vilao.vida -= self.personagem.dano
                if self.vilao.vida < 0:
                    self.vilao.vida = 0
                    self.vilao.brilho = True                

    def setup(self):
        texture = arcade.load_texture('Extras/Imagens/BotaoPause.png')
        hovered_texture = arcade.load_texture('Extras/Imagens/BotaoPauseHover.png')
        pressed_texture = arcade.load_texture('Extras/Imagens/BotaoPause.png')
        self.botao = Botao_Loja(self, Menu_Loja(), 1248, 688, texture, hovered_texture, pressed_texture)        
        self.ui_Manager.add_ui_element(self.botao)
        vilao_derrotado = open("Extras/Saves/Vilaoderrotado.txt", "r")
        self.qtd_derrotas = int(vilao_derrotado.read())
        vilao_derrotado.close()
        boss = random.randint(1, 6)
        if self.qtd_derrotas == 0:
            self.vilao = Vilao(900, 400, self.lista_monstros[random.randint(0, 3)], 
                                        random.randint(self.vida_min, self.vida_max), 
                                        random.randint(self.dano_min, self.dano_max))
        if self.qtd_derrotas != 0:
            for i in range(0, self.qtd_derrotas):
                self.vida_min *= 2
                self.vida_max *= 2
                self.dano_min *= 2
                self.dano_max *= 2
            if boss == 5:
                self.vilao = Vilao(900, 400, self.lista_boss[random.randint(0, 1)], 
                                        random.randint(self.vida_min*3, self.vida_max*3), 
                                        random.randint(self.dano_min*3, self.dano_max*3))
            else:
                self.vilao = Vilao(900, 400, self.lista_monstros[random.randint(0, 3)], 
                                    random.randint(self.vida_min, self.vida_max), 
                                    random.randint(self.dano_min, self.dano_max))
        self.personagem = Personagem(300, 400, "Extras/Imagens/Andy.png")
        self.lista_personagem = arcade.SpriteList()
        self.lista_personagem.append(self.vilao)
        self.lista_personagem.append(self.personagem)
        
        arq_vida = open("Extras/Saves/Savevida.txt", "r")
        self.item_vida = int(arq_vida.read())
        arq_vida.close()
        arq_forca = open("Extras/Saves/Saveforca.txt", "r")
        self.item_forca = int(arq_forca.read())
        arq_forca.close()
        for i in range(0, self.item_vida):
            self.personagem.vida_maxima *= 2
            self.personagem.vida = self.personagem.vida_maxima
        for j in range(0, self.item_forca):
            self.personagem.dano *= 2
        
        

    def on_hide_view(self):
        self.ui_Manager.unregister_handlers()
        numero = str(self.personagem.qtd_de_clicks)
        self.arq_cliques = open("Extras/Saves/Savecliques.txt", "w")
        self.arq_cliques.write(numero)
        self.arq_cliques.close()


class Menu_Loja(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_Manager = UIManager()
        self.qtd_de_clicks = 0
        self.qtd_de_moedas = 0

    def on_show_view(self):
        self.setup()

    def on_update(self, delta_time):
        arq_cliques = open("Extras/Saves/Savecliques.txt", "r")
        self.qtd_de_clicks = int(arq_cliques.read())
        arq_cliques.close()
        
        arq_moedas = open("Extras/Saves/Savemoeda.txt", "r")
        self.qtd_de_moedas = int(arq_moedas.read())
        arq_moedas.close()

    def on_draw(self):
        arcade.start_render()
        self.background = arcade.load_texture("Extras/Imagens/Background3.png")
        self.item_cura = arcade.load_texture("Extras/Imagens/Item_Cura.png")
        self.item_forca = arcade.load_texture("Extras/Imagens/Item_Forca.png")
        arcade.draw_lrwh_rectangle_textured(0, 0, 1280, 720, self.background)
        arcade.draw_lrwh_rectangle_textured(125, 220, 370, 370, self.item_cura)
        arcade.draw_lrwh_rectangle_textured(695, 220, 370, 370, self.item_forca)
    
        cliques = str(self.qtd_de_clicks)
        moedas = str(self.qtd_de_moedas)
        arcade.draw_text(cliques, 38, 700, arcade.color.WHITE, font_size=13)
        arcade.draw_text(moedas, 38, 672, arcade.color.WHITE, font_size=13)
        arcade.draw_text("200 MOEDAS", 880-92, 160, arcade.color.WHITE, font_size=35)
        arcade.draw_text("120 CLIQUES", 310-92, 160, arcade.color.WHITE, font_size=35)
    
        self.cursor = arcade.load_texture("Extras/Imagens/Cursor.png")
        self.moeda = arcade.load_texture("Extras/Imagens/Moeda.png")
        arcade.draw_texture_rectangle(15, 680, 26, 26, self.moeda)
        arcade.draw_texture_rectangle(20, 705, 30, 30, self.cursor)

    def setup(self):
        botao_Itemcura = Botao_Itemcura(self, "COMPRAR", 305, 100, 370, 75, id=None)
        self.ui_Manager.add_ui_element(botao_Itemcura)

        botao_Itemforca = Botao_Itemforca(self, "COMPRAR", 885, 100, 370, 75, id=None)
        self.ui_Manager.add_ui_element(botao_Itemforca)

        texture = arcade.load_texture('Extras/Imagens/BotaoPause.png')
        hovered_texture = arcade.load_texture('Extras/Imagens/BotaoPauseHover.png')
        pressed_texture = arcade.load_texture('Extras/Imagens/BotaoPause.png')
        botao = Botao_Sairloja(self, Jogo(), 1248, 688, texture, hovered_texture, pressed_texture)
        self.ui_Manager.add_ui_element(botao)

    def on_hide_view(self):
        self.ui_Manager.unregister_handlers()


class Gameover(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_Manager = UIManager()

    def on_show_view(self):
        self.setup()
    
    def on_draw(self):
        arcade.start_render()
        self.background = arcade.load_texture("Extras/Imagens/Background1.png")
        arcade.draw_lrwh_rectangle_textured(0, 0, 1280, 720, self.background)

    def setup(self):
        botao_restart = Botao_Gameover(self, Menu_Principal(), "REINICIAR", hori//2, vert//2, 370, 75, id=None)
        self.ui_Manager.add_ui_element(botao_restart)

    def on_hide_view(self):
        self.ui_Manager.unregister_handlers()


class Botao(UIFlatButton):
    def __init__(self, text='aaa', x=1280//2, y=100, width=20, height=20, align="center", id=None):
        super().__init__(text, x, y, width, height, align, id)

    def on_click(self):
        pass


class Botao_Loja(UIImageButton):
    def __init__(self, v, n, x, y, texture, hover_texture, press_texture):
        super().__init__(x, y, texture, hover_texture, press_texture)
        self.next_view = n
        self.view = v
        self.vilao_morto = False
    
    def set_vilao_morto(self):
        self.vilao_morto = not self.vilao_morto

    def on_click(self):
        if self.vilao_morto == True:
            self.view.window.show_view(self.next_view)
        else:
            pass


class Botao_Sairloja(UIImageButton):
    def __init__(self, v, n, x, y, texture, hover_texture, press_texture):
        super().__init__(x, y, texture, hover_texture, press_texture)
        self.next_view = n
        self.view = v

    def on_click(self):
        self.view.window.show_view(self.next_view)


class Botao_MenuPrincipal(UIImageButton):
    def __init__(self, v, n, x, y, texture, hover_texture, press_texture):
        super().__init__(x, y, texture, hover_texture, press_texture)
        self.next_view = n
        self.view = v

    def on_click(self):
        self.view.window.show_view(self.next_view)


class Botao_Jogar(Botao):
    def __init__(self, v, n, text='aaa', x=hori//2, y=420, width=80, height=80, align="center", id=None):
        super().__init__(text, x, y, width, height, align, id)
        self.view = v
        self.next_view = n

        self.style.set_class_attrs(
    id, 
    font_size=38, 
    font_name='Candara', 
    font_color=arcade.color.WHITE, 
    font_color_hover=arcade.color.WHITE, 
    font_color_press=arcade.color.WHITE, 
    bg_color=arcade.color.ALIZARIN_CRIMSON,
    bg_color_hover=arcade.color.ALIZARIN_CRIMSON,
    bg_color_press=arcade.color.ALIZARIN_CRIMSON,
    border_color_hover=arcade.color.WHITE,
    border_color_press=arcade.color.WHITE)
    
    def on_click(self):
        self.view.window.show_view(self.next_view)


class Botao_sair(Botao):
    def __init__(self, text='aaa', x=hori//2, y=420, width=80, height=80, align="center", id=None):
        super().__init__(text, x, y, width, height, align, id)

        self.style.set_class_attrs(
    id, 
    font_size=38, 
    font_name='Candara', 
    font_color=arcade.color.WHITE, 
    font_color_hover=arcade.color.WHITE, 
    font_color_press=arcade.color.WHITE, 
    bg_color=arcade.color.ALIZARIN_CRIMSON,
    bg_color_hover=arcade.color.ALIZARIN_CRIMSON,
    bg_color_press=arcade.color.ALIZARIN_CRIMSON,
    border_color_hover=arcade.color.WHITE,
    border_color_press=arcade.color.WHITE)
    
    def on_click(self):
        arcade.close_window()


class Botao_Itemforca(Botao):
    def __init__(self, v, text='aaa', x=hori//2, y=420, width=80, height=80, align="center", id=None):
        super().__init__(text, x, y, width, height, align, id)
        self.view = v
        self.style.set_class_attrs(
        id, 
        font_size=38, 
        font_name='Candara', 
        font_color=arcade.color.WHITE, 
        font_color_hover=arcade.color.WHITE, 
        font_color_press=arcade.color.WHITE, 
        bg_color=arcade.color.EBONY,
        bg_color_hover=arcade.color.EBONY,
        bg_color_press=arcade.color.EBONY,
        border_color_hover=arcade.color.WHITE,
        border_color_press=arcade.color.WHITE)      

    def on_click(self):
        self.arq_moedas = open("Extras/Saves/Savemoeda.txt", "r")
        self.qtd_de_moedas = int(self.arq_moedas.read())
        self.arq_moedas.close()
        self.arq_forca = open("Extras/Saves/Saveforca.txt", "r")
        self.item_forca = int(self.arq_forca.read())
        self.arq_forca.close()  
        if self.qtd_de_moedas >= 200:
            self.item_forca += 1
            str_forca = str(self.item_forca)
            self.arq_forca = open("Extras/Saves/Saveforca.txt", "w")
            self.arq_forca.write(str_forca)
            self.arq_forca.close()
            arq_moedas = open("Extras/Saves/Savemoeda.txt", "w")
            qtd_de_moedas = self.qtd_de_moedas - 200
            arq_moedas.write(str(qtd_de_moedas))
            self.arq_moedas.close()       
        else:
            pass


class Botao_Itemcura(Botao):
    def __init__(self, v, text='aaa', x=hori//2, y=420, width=80, height=80, align="center", id=None):
        super().__init__(text, x, y, width, height, align, id)
        self.view = v

        self.style.set_class_attrs(
        id, 
        font_size=38, 
        font_name='Candara', 
        font_color=arcade.color.WHITE, 
        font_color_hover=arcade.color.WHITE, 
        font_color_press=arcade.color.WHITE, 
        bg_color=arcade.color.EBONY,
        bg_color_hover=arcade.color.EBONY,
        bg_color_press=arcade.color.EBONY,
        border_color_hover=arcade.color.WHITE,
        border_color_press=arcade.color.WHITE)
    
    def on_click(self):
        arq_clicks = open("Extras/Saves/Savecliques.txt", "r")
        qtd_de_clicks = int(arq_clicks.read())
        arq_clicks.close()

        arq_vida = open("Extras/Saves/Savevida.txt", "r")
        item_vida = int(arq_vida.read())
        arq_vida.close()
        self.save_vida = item_vida

        if qtd_de_clicks >= 120:
            item_vida += 1
            str_vida = str(item_vida)

            arq_vida = open("Extras/Saves/Savevida.txt", "w")
            arq_vida.write(str_vida)
            arq_vida.close()

            arq_clicks = open("Extras/Saves/Savecliques.txt", "w")
            qtd_de_clicks -= 120
            arq_clicks.write(str(qtd_de_clicks))
            arq_clicks.close()     
        else:
            pass


class Botao_Gameover(Botao):
    def __init__(self, v, n, text='aaa', x=hori//2, y=420, width=80, height=80, align="center", id=None):
        super().__init__(text, x, y, width, height, align, id)
        self.view = v
        self.next_view = n

        self.style.set_class_attrs(
    id, 
    font_size=38, 
    font_name='Candara', 
    font_color=arcade.color.WHITE, 
    font_color_hover=arcade.color.WHITE, 
    font_color_press=arcade.color.WHITE, 
    bg_color=arcade.color.ALIZARIN_CRIMSON,
    bg_color_hover=arcade.color.ALIZARIN_CRIMSON,
    bg_color_press=arcade.color.ALIZARIN_CRIMSON,
    border_color_hover=arcade.color.WHITE,
    border_color_press=arcade.color.WHITE)
    
    def on_click(self):
        self.view.window.show_view(self.next_view)

        arq_forca = open("Extras/Saves/Saveforca.txt", "w")
        arq_forca.write("0")
        arq_forca.close()

        arq_moedas = open("Extras/Saves/Savemoeda.txt", "w")
        arq_moedas.write("0")
        arq_moedas.close()

        arq_cliques = open("Extras/Saves/Savecliques.txt", "w")
        arq_cliques.write("0")
        arq_cliques.close()

        arq_vida = open("Extras/Saves/Savevida.txt", "w")
        arq_vida.write("0")
        arq_vida.close()

        arq_vilao = open("Extras/Saves/Vilaoderrotado.txt", "w")
        arq_vilao.write("0")
        arq_vilao.close()


if __name__ == "__main__":
    window = arcade.Window(hori, vert, titu)
    menu = Menu_Principal()
    window.show_view(menu)
    arcade.run()