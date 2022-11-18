import pygame as pg
from pygame.event import custom_type, Event


evento_TPS = Event(custom_type(), {'delta_time': int})