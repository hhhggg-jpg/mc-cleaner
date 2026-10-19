#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MC存档清理器 - Kivy版 (纯Python，无numpy依赖，方便打包APK)
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
import random, math

# ============ 纯Python柏林噪声 ============
class PerlinNoise:
    def __init__(self, seed=0):
        rng = random.Random(seed & 0xFFFFFFFF)
        p = list(range(256))
        rng.shuffle(p)
        self.p = p + p

    def fade(self, t): return t*t*t*(t*(t*6-15)+10)
    def lerp(self, t, a, b): return a+t*(b-a)
    def grad(self, h, x, y):
        u = x if h<4 else y
        v = y if h<4 else x
        return ((u if h&1==0 else -u) + (v if h&2==0 else -v))

    def noise2d(self, x, y):
        X = int(math.floor(x)) & 255
        Y = int(math.floor(y)) & 255
        x -= math.floor(x); y -= math.floor(y)
        u, v = self.fade(x), self.fade(y)
        A = self.p[X]+Y; B = self.p[X+1]+Y
        return self.lerp(v,
            self.lerp(u, self.grad(self.p[A],x,y), self.grad(self.p[B],x-1,y)),
            self.lerp(u, self.grad(self.p[A+1],x,y-1), self.grad(self.p[B+1],x-1,y-1)))

    def fbm(self, x, y, oct=4):
        t, f, a, m = 0, 1, 1, 0
        for _ in range(oct):
            t += self.noise2d(x*f, y*f)*a
            m += a; a *= 0.5; f *= 2
        return t/m


class CleanUI(BoxLayout):
    def __init__(self, **kw):
        super().__init__(orientation='vertical', **kw)
        self.seed = 0
        self.add_widget(Label(text='MC存档清理器 Pro', size_hint=(1,0.08), font_size=24))
        self.info = Label(text='输入种子，生成地形预览', size_hint=(1,0.1))
        self.add_widget(self.info)

        btn_row = BoxLayout(size_hint=(1,0.1))
        btn_row.add_widget(Button(text='输入种子', on_press=self.input_seed))
        btn_row.add_widget(Button(text='生成地形', on_press=self.gen_preview))
        self.add_widget(btn_row)

        self.img = Image(size_hint=(1,0.74))
        self.add_widget(self.img)

    def input_seed(self, *a):
        from kivy.uix.popup import Popup
        from kivy.uix.textinput import TextInput
        ti = TextInput(text=str(self.seed), multiline=False)
        pop = Popup(title='输入种子', content=ti, size_hint=(0.8,0.4))
        def done(*x):
            try: self.seed = int(ti.text)
            except: pass
            pop.dismiss()
        pop.content = BoxLayout(orientation='vertical')
        pop.content.add_widget(ti)
        pop.content.add_widget(Button(text='确定', on_press=done))
        ti.bind(on_text_validate=done)
        pop.open()

    def gen_preview(self, *a):
        pn = PerlinNoise(self.seed or 12345)
        size = 128
        pixels = []
        for j in range(size):
            for i in range(size):
                h = pn.fbm(i/16, j/16)
                v = int((h+1)*127)
                if v<80: c=(30,60,150)
                elif v<110: c=(40,150,60)
                elif v<140: c=(120,140,50)
                elif v<180: c=(100,80,40)
                else: c=(240,240,250)
                pixels.extend(c)
        tex = Texture.create(size=(size,size))
        tex.flip_vertical()
        tex.blit_buffer(bytes(pixels), colorfmt='rgb', bufferfmt='ubyte')
        self.img.texture = tex
        self.info.text = f'种子:{self.seed} 地形已生成'


class MCleanerApp(App):
    def build(self):
        return CleanUI()


if __name__ == '__main__':
    MCleanerApp().run()
