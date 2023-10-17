import yaml
from midigen.notes import Note
from midigen.keys import Key, Mode
from midigen.time import TimeSignature, Measure
from midigen.sequencer import Song, Track


def main():
    data = read_yaml()
    create_file(data)


def read_yaml():
    with open('yaml/test.yaml', 'r') as file:
        data = yaml.safe_load(file)
        print(data)
        return data


def create_progression_from_yaml(data):
    chords = []
    sections = {}
    for s in data['Sections']:
        sections[s] = []
        for block in data['Sections'][s]:
            parts = block.split('x')
            chord = int(parts[0].strip())
            bars = int(parts[1].strip())
            sections[s] += [chord] * bars
    for s in data['Format']:
        chords += sections[s]
    return chords


def create_file(data):
    filename = "song"
    key = Key(Note[data['Key']], Mode[data['Mode']])
    ts = [int(x) for x in data['TimeSignature'].split('/')]
    time_signature = TimeSignature(*ts)
    tempo = data['Tempo']
    progression = create_progression_from_yaml(data)

    chords = Track.from_measures([
        Measure.from_pattern(
            # input full bar instead of 4 quarter notes
            pattern=[
                key.relative_key(degree).chord(
                    # default chords are the base triad - try adding extensions
                    # extensions=[7],
                    # pick a voicing close to the root triad
                    match_voicing=key.triad()
                )
            ] * time_signature.numerator,
            time_signature=time_signature,
            velocity=90
        )
        for degree in progression
    ])

    # write the song to a MIDI file
    # todo: separate filename and metadata?
    Song([chords]).to_midi(f'output_files/{filename}.mid', tempo=tempo)


if __name__ == "__main__":
    main()
