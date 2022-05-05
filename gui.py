from generator import generate_thumbnail


def main():
    generate_thumbnail(
        'Example/nature-underwater-dolphin-animal-aquarium-zoo-blue-104839-full.mp4',
        output_dir='Example',
        flat_dir=True # Create all thumbnails into one directory
    )


if __name__ == "__main__":
    main()
