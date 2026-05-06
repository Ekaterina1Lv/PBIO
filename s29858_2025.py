# Numer albumu: s29858
# Data: 30.04.2026
# Opis: Generator losowych sekwencji DNA w formacie FASTA z analizą statystyczną

import random

def generate_sequence(length: int) -> str:
    """Zwraca losową sekwencję DNA o zadanej długości."""
    nucleotides = ['A', 'C', 'G', 'T']
    return ''.join(random.choice(nucleotides) for _ in range(length))

def calculate_stats(sequence: str) -> dict:
    """Zwraca słownik ze statystykami sekwencji.
    Klucze: "A", "C", "G", "T" (wartości float, %),
    "GC" (wartość float, %)."""
    total = len(sequence)
    stats = {base: (sequence.count(base) / total * 100) for base in 'ACGT'}
    stats["gc_ratio_A"] = stats["G"]+stats["C"]
    return stats

def insert_name(sequence: str, name: str) -> str:
    """Wstawia imię w losową pozycję sekwencji.
    Imię zapisane małymi literami."""
    position = random.randint(0, len(sequence))
    name_lower = name.lower()
    return sequence[:position] + name_lower + sequence[position:]

def format_fasta(seq_id: str, description: str,
    sequence: str, line_width: int = 80) -> str:
    """Zwraca sformatowany rekord FASTA jako string."""
    header = f">{seq_id} {description}".strip()
    lines = [sequence[i:i+line_width] for i in range(0, len(sequence), line_width)]
    return header + "\n" + "\n".join(lines) + "\n# EOF_1"



def validate_positive_int(prompt: str,
    min_val: int = 1,
    max_val: int = 100_000) -> int:
    """Pobiera od użytkownika liczbę całkowitą z zakresu.
    W przypadku błędu powtarza pytanie."""

    while True:
        value = input(prompt)
        if not value.isdigit():
            print("Błąd: wartość musi być liczbą całkowitą z zakresu [1, 100000].")
            continue
        value = int(value)
        if value < min_val or value > max_val:
            print("Błąd: wartość musi być liczbą całkowitą z zakresu [1, 100000].")
            continue
        return value

def validate_id(seq_id: str) ->str:
    while " " in seq_id or seq_id == "":
        print("ID nie może zawierać spacji.")
        seq_id = input("Podaj ID sekwencji: ")
    return seq_id

def main():
    """Wiadomo."""
    length = validate_positive_int("Podaj długość sekwencji: ")
    seq_id = input("Podaj ID sekwencji: ")
    seq_id = validate_id(seq_id)
    description = input("Podaj opis sekwencji: ")
    name = input("Podaj imię: ")
    sequence = generate_sequence(length)
    stats = calculate_stats(sequence)
    sequence_with_name = insert_name(sequence, name)
    fasta_text = format_fasta(seq_id, description, sequence_with_name)
    with open(f"{seq_id}.fasta", "w") as f:
        f.write(fasta_text)
    print(f"\nSekwencja zapisana do pliku: {seq_id}.fasta\n")

    print(f"Statystyki sekwencji (n={length}):")
    for base in "ACGT":
        print(f"{base}: {stats[base]:.2f}%")

    print(f"GC-content: {stats['gc_ratio_A']:.2f}%")

    

