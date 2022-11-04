import pygame as pg
from configuracoes import Configuracoes
from entidades.arma.faca import Faca
from entidades.arma.pistola import Pistola
from spritesheet import Spritesheet
from .entidade import Entidade


class Jogador(Entidade):
    def __init__(self, fase, pos, groups, obstacle_sprites, screen) -> None:
        super().__init__(groups)

        fase.registrar_evento(pg.KEYUP, self.evento_tecla_solta)
        fase.registrar_evento(pg.KEYDOWN, self.evento_tecla_apertada)
        fase.registrar_evento(pg.MOUSEBUTTONDOWN, self.evento_mouse)

        self.__fase = fase
        self.__configuracoes = Configuracoes()

        # Imagem e hitbox
        self.__spritesheet = Spritesheet("skelet", 1)
        self.image = self.image('idle_0.png')
        self.animations = self.__spritesheet.animation_frames
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -8)

        self.obstacle_sprites = obstacle_sprites

        # Movimento
        self.velocidade = 5

        self.vida = 3
        self.vulneravel = True
        self.hurt_time = None
        self.duracao_invencibilidade = 300
        self.morto = False

        # Dash
        self.__impulso_disponivel = True
        self.__esta_com_impulso = False
        self.__duracao_do_impulso = 100
        self.__duracao_de_recarga_do_impulso = 1000
        self.__tempo_do_impulso = None

        # Ataque
        self.__esta_atacando = False
        self.__attack_cd = 400
        self.__tempo_do_ataque = None

        # Animação
        self.__status = 'right'

        # Armas
        self.__faca = Faca()
        self.__pistola = Pistola(self.fase, [self.fase.grupo_de_entidade])

        self.__janela = screen

    def evento_tecla_solta(self, evento):
        # Entradas de movimentação:
        if evento.key == pg.K_w or evento.key == pg.K_s:
            self.direction.y = 0
        elif evento.key == pg.K_a or evento.key == pg.K_d:
            self.direction.x = 0

    def evento_tecla_apertada(self, evento):
        if evento.key == pg.K_w:
            self.direction.y = -1
        elif evento.key == pg.K_s:
            self.direction.y = 1
        elif evento.key == pg.K_a:
            self.direction.x = -1
            self.__status = 'left'
        elif evento.key == pg.K_d:
            self.__status == 'right'
            self.direction.x = 1

        if evento.key == pg.K_s and not self.__esta_com_impulso:
            self.__esta_com_impulso = False
            self.__tempo_do_impulso = pg.time.get_ticks()

    def evento_mouse(self, evento):
        if evento.type == pg.MOUSEBUTTONDOWN:
            if evento.button == 1:
                self.atacar(self.__pistola)

    @property
    def tipo(self):
        return "jogador"

    @property
    def fase(self):
        return self.__fase

    @property
    def pos_mouse(self):
        return pg.mouse.get_pos()

    def image(self, sprite: str):
        return self.__spritesheet.get_sprite(sprite)

    def status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.__status and not 'attack' in self.__status:
                self.__status += '_idle'
        else:
            if 'idle' in self.__status:
                self.__status = self.__status.replace('_idle', '')

        if self.__esta_atacando:
            self.direction.x = 0
            self.direction.y = 0
        #     if not 'attack' in self.__status:
        #         if 'idle' in self.__status:
        #             self.__status = self.__status.replace('_idle', '_attack')
        #         else:
        #             self.__status += '_attack'
        # else:
        #     if 'attack' in self.__status:
        #         self.__status = self.__status.replace('_attack', '')

    def dash(self):
        if self.__dashing and self.__active_dash:
            self.__velocidade = 20

    def cooldowns(self):
        current_time = pg.time.get_ticks()
        # Controla o tempo de recarga dos ataques:
        if self.__esta_atacando:
            if current_time - self.__tempo_do_ataque >= self.__attack_cd:
                self.__esta_atacando = False

        """ 
        if self.__esta_com_impulso:
            if current_time - self.__dash_time >= self.__dash_duration:
                self.__dashing = False
                self.__velocidade = 5
        if not self.__active_dash:
            if current_time - self.__dash_time >= self.__dash_cd:
                self.__active_dash = True
        """

        if not self.vulneravel:
            if current_time - self.hurt_time >= self.duracao_invencibilidade:
                self.vulneravel = True

    def animate(self):
        animation = self.animations[self.__status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]

        # Oscila a visibilidade quando é atacado
        if not self.vulneravel:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)   

    def atacar(self, arma):
        if not self.__esta_atacando:
            self.__esta_atacando = True
            self.__tempo_do_ataque = pg.time.get_ticks()
            
            if type(arma) == Pistola:
                self.__pistola.atirar(self.pos_mouse)
            elif type(arma) == Faca:
                pass

    def check_death(self):
        if self.vida <= 0:
            self.morto = True
            self.kill()

    def atualizar(self, tempo_passado):        
        self.move()
        self.cooldowns()
        self.status()
        self.animate()
        self.check_death()
        self.__pistola.mover(self.rect.center, self.pos_mouse)

    def desenhar(self):
        return (self,)

    # Desenha a quantidade de vidas restantes do player

    def barra_de_vida(self):
        escala = self.__configuracoes.tamanho_tile * 1.5
        coracao_imagem = pg.image.load('sprites/coracao.png').convert_alpha()
        coracao_imagem = pg.transform.scale(coracao_imagem, (escala, escala))
        for c in range(self.__jogador.vida):
            self.display_surface.blit(coracao_imagem, (c * 50, 0))
