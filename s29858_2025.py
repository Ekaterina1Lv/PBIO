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
    if description:
        header = f">{seq_id} {description}"
    else:
        header = f">{seq_id}"
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

def find_motif(sequence: str, motif: str) -> list:
    positions = []
    for i in range(len(sequence) - len(motif) + 1):
        if sequence[i:i+len(motif)] == motif:
            positions.append(i + 1)
    return positions

def complement(sequence: str) -> str:
    mapping = {'A':'T','T':'A','C':'G','G':'C'}
    return ''.join(mapping[b] for b in sequence)


def reverse_complement(sequence: str) -> str:
    return complement(sequence)[::-1]

def batch_mode(num_sequences: int, base_id: str, description: str,
               seq_length: int, name: str) -> list:
    """Generuje wiele sekwencji i zwraca listę sformatowanych rekordów FASTA."""
    all_records = []
    for i in range(1, num_sequences + 1):
        seq_id = f"{base_id}_{i:03d}"
        sequence = generate_sequence(seq_length)
        sequence_with_name = insert_name(sequence, name)
        record = format_fasta(seq_id, description, sequence_with_name)
        all_records.append(record)

        stats = calculate_stats(sequence)
        print(f"\nStatystyki {seq_id} (n={seq_length}):")
        for base in "ACGT":
            print(f"  {base}: {stats[base]:.2f}%")
        print(f"  GC-content: {stats['gc_ratio_A']:.2f}%")

    return all_records

def transcribe_dna(sequenc: str) -> str:
    """Transkrypcja DNA do mRNA."""
    return sequenc.replace('T', 'U')


def main():
    """Wiadomo."""
    length = validate_positive_int("Podaj długość sekwencji: ")

    seq_id = input("Podaj ID sekwencji: ")
    seq_id = validate_id(seq_id)

    description = input("Podaj opis sekwencji: ")
    name = input("Podaj imię: ")
    while name.strip() == "":
        print("Imię nie może być puste.")
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
        print(f"  {base}: {stats[base]:.2f}%")
    print(f"GC-content: {stats['gc_ratio_A']:.2f}%")

    positions = []

    if input("Czy chcesz wyszukać motyw? (t/n): ").lower() == 't':
        motif = input("Podaj motyw do wyszukania: ").upper()

        while len(motif) == 0 or any(base not in "ACGT" for base in motif):
            print("Motyw może zawierać tylko A C G T!")
            motif = input("Podaj motyw: ").upper()

        positions = find_motif(sequence, motif)

        if positions:
            print(f"Motyw '{motif}' znaleziony na pozycjach: {positions}")
        else:
            print(f"Motyw '{motif}' nie występuje w sekwencji")

    if input("Czy wygenerować sekwencję komplementarną? (t/n): ").lower() == 't':
        comp_seq = complement(sequence)
        rev_comp_seq = reverse_complement(sequence)

        print("\nSekwencja komplementarna:")
        print(comp_seq)

        print("\nSekwencja odwrotnie komplementarna:")
        print(rev_comp_seq)

        with open(f"{seq_id}.fasta", "a") as f:
            f.write("\n")
            f.write(format_fasta(seq_id + "_COMP", "komplementarna", comp_seq))

            f.write("\n")
            f.write(format_fasta(seq_id + "_REVCOMP", "reverse complement", rev_comp_seq))

    if input("Czy uruchomić batch mode? (t/n): ").lower() == 't':
        num_seq = validate_positive_int("Ile sekwencji?: ", 1, 100)

        base_id = input("Podaj bazowe ID: ")
        base_id = validate_id(base_id)

        records = batch_mode(num_seq, base_id, description, length, name)

        filename = f"{base_id}_batch.fasta"

        with open(filename, 'w') as f:
            f.write("\n".join(records))

        print(f"Zapisano {num_seq} sekwencji do {filename}")

    if input("Czy wygenerować mRNA? (t/n): ").lower() == 't':
        mrna = transcribe_dna(sequence)

        print("\nmRNA:")
        print(mrna)

        with open(f"{seq_id}.fasta", "a") as f:
            f.write("\n")
            f.write(format_fasta(seq_id + "_mRNA", "transcription", mrna))

if __name__ == "__main__":
    main()
