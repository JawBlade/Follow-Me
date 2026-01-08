def main():
    from ultralytics import YOLO

    model = YOLO('Human-50e-11n.pt')
    print(f"Model Input Size: {model.overrides['imgsz']}")

    r1 = model('frontleft_fisheye_image.jpg', save=True, show=True)

    r2 = model('frontright_fisheye_image.jpg', save=True, show=True)

if __name__ == '__main__':
    main()