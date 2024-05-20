MAP_VALID_VALS = {
    "content": {
        "figure": '{works.map((artwork) => (\n<figure className="shrink-0" key={artwork.artist}>\n<div className="overflow-hidden rounded-md"\n<Image src={artwork.art} alt={`Photo by {artwork.artist}`} width={300} height={400} className="aspect-[3/4] h-fit w-fit object-cover" />\n</div>\n<figcaption className="pt-2 text-xs text-muted-foreground">\nPhoto by\n<span className="font-semibold text-foreground">\n{artwork.artist}\n</span>\n</figcaption>\n</figure>\n))}',
        "div": "{tags.map((tag) => (\n<div>\nTest {tag}\n</div>\n))}",
        "label": '{tags.map((tag) => (\n<Label htmlFor="test">\nTest {tag}\n</Label>\n))}',
        "image": '{tags.map((tag) => (\n<Image src={test} alt="This is a test image" width={200} height={200} />\n))}',
    },
    "imports": {
        "none": [""],
        "image": ["import Image from 'next/image'"],
    },
}


JS_VALID_VALS_MAP = {
    "map": MAP_VALID_VALS,
}
