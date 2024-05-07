HTML_CONTENT_VALID_VALS = {
    "content": {
        "h1": '<h1 className="font-semibold text-foreground">\n{artwork.artist}\n</h1>',
        "h2": '<h2 className="font-semibold text-foreground">\n{artwork.artist}\n</h2>',
        "h3": '<h3 className="font-semibold text-foreground">\n{artwork.artist}\n</h3>',
        "h4": '<h4 className="font-semibold text-foreground">\n{artwork.artist}\n</h4>',
        "h5": '<h5 className="font-semibold text-foreground">\n{artwork.artist}\n</h5>',
        "h6": '<h6 className="font-semibold text-foreground">\n{artwork.artist}\n</h6>',
        "p": '<p className="font-semibold text-foreground">\n{artwork.artist}\n</p>',
        "span": '<span className="font-semibold text-foreground">\n{artwork.artist}\n</span>',
        "text_standard": """<span className="font-semibold text-foreground">\nThis is a long string and {`I'm`} {testing} it\n</span>""",
        "no_styles": "<h1>\nThis is a long string for {testing}\n</h1>",
    }
}

DIV_VALID_VALS = {
    "content": {
        "simple": "<div>\nThis is a long test string {`I'm`} testing\n</div>",
        "with_styles": '<div className="w-80">\nThis is a {test} string\n</div>',
        "shell": "<>\nThis is a shell test\n</>",
        "map": "<div key={tag}>\n{tags.map((tag) => (\n<h4>\nAn epic {tag} heading\n</h4>\n))}\n</div>",
        "label": '<div>\n<Label htmlFor="example">\nA test {label}\n</Label>\n</div>',
        "multi_items": '<div>\nThis is a\n<span className="red-500">\ncomplete {test}\n</span>\n<Label htmlFor="name">\nFirst name\n</Label>\n{tags.map((tag) => (\n<h4>\nAn epic {tag} heading\n</h4>\n))}\n<Label htmlFor="email">\nEmail address\n</Label>\n</div>',
        "multi_html": '<div className="w-8 h-12">\n<h1>\nTest h1 {tag}\n</h1>\n<figure className="shrink-0" key={artwork.artist}>\n<div className="overflow-hidden rounded-md"\n<Image src={artwork.art} width={300} height={400} alt={`Photo by {artwork.artist}`} className="aspect-[3/4] h-fit w-fit object-cover" />\n</div>\n<figcaption className="pt-2 text-xs text-muted-foreground">\nPhoto by\n<span className="font-semibold text-foreground">\n{artwork.artist}\n</span>\n</figcaption>\n</figure>\n<h2>\nTest h2 tag\n</h2>\n</div>',
    },
    "imports": {
        "label": 'import { Label } from "@/components/ui/label"',
        "multi_items": 'import { Label } from "@/components/ui/label"',
    },
}

FIG_CAPTION_VALID_VALS = {
    "content": {
        "multi_text": '<figcaption className="pt-2 text-xs text-muted-foreground">\nPhoto by\n<span className="font-semibold text-foreground">\n{artwork.artist}\n</span>\n</figcaption>',
        "text_html_content": '<figcaption className="pt-2 text-xs text-muted-foreground">\n<h1>\ntest {here}\n</h1>\n</figcaption>',
        "standard": '<figcaption className="pt-2 text-xs text-muted-foreground">\nPhoto by author\n</figcaption>',
        "standard_with_params": '<figcaption className="pt-2 text-xs text-muted-foreground">\nPhoto by {author}\n</figcaption>',
        "no_styles": "<figcaption>\nPhoto by author\n</figcaption>",
    },
}

FIGURE_VALID_VALS = {
    "content": {
        "complete": '<figure className="shrink-0" key={artwork.artist}>\n<div className="overflow-hidden rounded-md"\n<Image src={artwork.art} width={300} height={400} alt={`Photo by {artwork.artist}`} className="aspect-[3/4] h-fit w-fit object-cover" />\n</div>\n<figcaption className="pt-2 text-xs text-muted-foreground">\nPhoto by\n<span className="font-semibold text-foreground">\n{artwork.artist}\n</span>\n</figcaption>\n</figure>',
        "no_key": '<figure className="shrink-0">\n<div className="overflow-hidden rounded-md"\n<Image src={artwork.art} width={300} height={400} alt={`Photo by {artwork.artist}`} className="aspect-[3/4] h-fit w-fit object-cover" />\n</div>\n<figcaption className="pt-2 text-xs text-muted-foreground">\nPhoto by\n<span className="font-semibold text-foreground">\n{artwork.artist}\n</span>\n</figcaption>\n</figure>',
        "no_styles": '<figure>\n<div className="overflow-hidden rounded-md"\n<Image src={artwork.art} width={300} height={400} alt={`Photo by {artwork.artist}`} className="aspect-[3/4] h-fit w-fit object-cover" />\n</div>\n<figcaption className="pt-2 text-xs text-muted-foreground">\n<h1 className="font-semibold text-foreground">\nPhoto by me\n</h1>\n</figcaption>\n</figure>',
        "simple_basic_url": '<figure>\n<Image src={artwork.art} width={300} height={400} alt="Photo by me" />\n<figcaption>\nPhoto by author\n</figcaption>\n</figure>',
        "simple_static_img": '<figure>\n<Image src={profilePic} width={300} height={400} alt="Photo by me" />\n<figcaption>\nPhoto by\n<span>\nAn awesome person\n</span>\n</figcaption>\n</figure>',
    },
    "imports": {
        "basic": "import Image from 'next/image'",
        "static_img": "import Image from 'next/image'\nimport profilePic from './me.png'",
    },
}

HTML_VALID_VALS_MAP = {
    "html_content": HTML_CONTENT_VALID_VALS,
    "div": DIV_VALID_VALS,
    "figcaption": FIG_CAPTION_VALID_VALS,
    "figure": FIGURE_VALID_VALS,
}
