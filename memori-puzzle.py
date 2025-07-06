from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
import random

class MemoryGame(App):
    def build(self):
        # Atur warna latar belakang gelap
        Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Hitam pekat
        
        # Layout utama
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Panel skor
        score_panel = BoxLayout(size_hint=(1, 0.1))
        self.score_label = Label(
            text="Pasangan Ditemukan: 0", 
            font_size=16,  # Ukuran lebih kecil
            color=(1, 1, 1, 1)  # Putih
        )
        self.try_label = Label(
            text="Percobaan: 0", 
            font_size=16, 
            color=(1, 1, 1, 1)
        )
        score_panel.add_widget(self.score_label)
        score_panel.add_widget(self.try_label)
        
        # Grid kartu (4x4)
        self.grid = GridLayout(cols=4, spacing=5)
        self.cards = []
        self.selected = []
        self.matched_pairs = 0
        self.attempts = 0
        
        # Inisialisasi game
        self.symbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']  # Ganti emoji dengan huruf
        self.init_game()
        
        main_layout.add_widget(score_panel)
        main_layout.add_widget(self.grid)
        return main_layout
    
    def init_game(self):
        self.grid.clear_widgets()
        self.cards = []
        pairs = self.symbols * 2
        random.shuffle(pairs)
        
        for symbol in pairs:
            # Tombol kartu dengan desain lebih jelas
            card = Button(
                text='?',  # Default: tampilkan tanda tanya
                font_size=24,
                bold=True,
                background_color=(0.2, 0.6, 0.8, 1),  # Biru muda
                background_normal='',
                color=(0, 0, 0, 1)  # Teks hitam
            )
            card.symbol = symbol
            card.is_open = False
            card.bind(on_press=self.card_click)
            self.grid.add_widget(card)
            self.cards.append(card)
    
    def card_click(self, card):
        if len(self.selected) >= 2 or card.is_open:
            return
        
        # Buka kartu
        card.text = card.symbol
        card.is_open = True
        card.background_color = (0.9, 0.9, 0.3, 1)  # Kuning saat dipilih
        self.selected.append(card)
        
        if len(self.selected) == 2:
            self.attempts += 1
            self.try_label.text = f"Percobaan: {self.attempts}"
            
            if self.selected[0].symbol == self.selected[1].symbol:
                # Jika cocok
                self.matched_pairs += 1
                self.score_label.text = f"Pasangan Ditemukan: {self.matched_pairs}"
                for c in self.selected:
                    c.background_color = (0.3, 0.8, 0.3, 1)  # Hijau jika benar
                self.selected = []
                
                if self.matched_pairs == len(self.symbols):
                    self.show_win_message()
            else:
                # Jika tidak cocok, tunggu 1 detik lalu tutup
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt: self.close_cards(), 1.0)
    
    def close_cards(self):
        for card in self.selected:
            card.text = '?'
            card.is_open = False
            card.background_color = (0.2, 0.6, 0.8, 1)  # Kembalikan ke biru
        self.selected = []
    
    def show_win_message(self):
        win_layout = BoxLayout(orientation='vertical')
        win_label = Label(
            text=f"Menang!\nTotal Percobaan: {self.attempts}",
            font_size=24,
            color=(0, 1, 0, 1)  # Hijau
        )
        restart_btn = Button(
            text="Main Lagi",
            size_hint=(0.6, 0.2),
            background_color=(0.2, 0.5, 0.8, 1)
        )
        restart_btn.bind(on_press=lambda x: self.restart_game())
        win_layout.add_widget(win_label)
        win_layout.add_widget(restart_btn)
        self.root.clear_widgets()
        self.root.add_widget(win_layout)
    
    def restart_game(self):
        self.root.clear_widgets()
        self.matched_pairs = 0
        self.attempts = 0
        self.build()

if __name__ == '__main__':
    MemoryGame().run()
l