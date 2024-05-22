import pytest

from pydantic import ValidationError

from cli.templates.details import COMPONENT_DETAILS_DICT
from tests.mappings.ui_imports import VALID_IMPORTS
from tests.mappings.ui_vals import VALID_VALS_MAP
from tests.templates.helper import SimpleCompBuilder

from zentra.nextjs import Image, StaticImage
from zentra.ui.presentation import (
    Accordion,
    AccordionItem,
    AspectRatio,
    Avatar,
    Badge,
    Progress,
    Separator,
    Skeleton,
    SkeletonGroup,
    SkeletonShell,
    Table,
    TableCell,
    TableMap,
    TableMapRow,
    TableRow,
)


class TestSeparator:
    @pytest.fixture
    def separator(self) -> Separator:
        return Separator()

    @pytest.fixture
    def separator_full(self) -> Separator:
        return Separator(styles="mx-4", orientation="horizontal")

    @pytest.fixture
    def wrapper(self, separator: Separator) -> SimpleCompBuilder:
        return SimpleCompBuilder(separator, COMPONENT_DETAILS_DICT["Separator"])

    @pytest.fixture
    def wrapper_full(self, separator_full: Separator) -> SimpleCompBuilder:
        return SimpleCompBuilder(separator_full, COMPONENT_DETAILS_DICT["Separator"])

    @staticmethod
    def test_content_str(wrapper: SimpleCompBuilder):
        wrapper.run("content", VALID_VALS_MAP["separator"]["content"]["simple"])

    @staticmethod
    def test_content_str_full(wrapper_full: SimpleCompBuilder):
        wrapper_full.run("content", VALID_VALS_MAP["separator"]["content"]["full"])

    @staticmethod
    def test_import_str(wrapper: SimpleCompBuilder):
        wrapper.run("imports", VALID_IMPORTS["separator"])


class TestAvatar:
    @pytest.fixture
    def avatar_url(self) -> Avatar:
        return Avatar(
            src="https://github.com/shadcn.png",
            alt="@shadcn",
            fallback_text="CN",
        )

    @pytest.fixture
    def avatar_path(self) -> Avatar:
        return Avatar(
            src="/profile.png",
            alt="Awesome photo of $.me",
            fallback_text="AA",
        )

    @pytest.fixture
    def avatar_static(self) -> Avatar:
        return Avatar(
            src=StaticImage(name="profilePic", path="./me.png"),
            alt="Awesome photo of $.me",
            fallback_text="AA",
        )

    @pytest.fixture
    def wrapper_url(self, avatar_url: Avatar) -> SimpleCompBuilder:
        return SimpleCompBuilder(avatar_url, COMPONENT_DETAILS_DICT["Avatar"])

    @pytest.fixture
    def wrapper_path(self, avatar_path: Avatar) -> SimpleCompBuilder:
        return SimpleCompBuilder(avatar_path, COMPONENT_DETAILS_DICT["Avatar"])

    @pytest.fixture
    def wrapper_static(self, avatar_static: Avatar) -> SimpleCompBuilder:
        return SimpleCompBuilder(avatar_static, COMPONENT_DETAILS_DICT["Avatar"])

    @staticmethod
    def test_content_str_url(wrapper_url: SimpleCompBuilder):
        wrapper_url.run("content", VALID_VALS_MAP["avatar"]["content"]["url"])

    @staticmethod
    def test_content_str_path(wrapper_path: SimpleCompBuilder):
        wrapper_path.run("content", VALID_VALS_MAP["avatar"]["content"]["path"])

    @staticmethod
    def test_content_str_static(wrapper_static: SimpleCompBuilder):
        wrapper_static.run("content", VALID_VALS_MAP["avatar"]["content"]["static_img"])

    @staticmethod
    def test_import_str_url(wrapper_url: SimpleCompBuilder):
        wrapper_url.run("imports", VALID_IMPORTS["avatar"]["path_n_url"])

    @staticmethod
    def test_import_str_path(wrapper_path: SimpleCompBuilder):
        wrapper_path.run("imports", VALID_IMPORTS["avatar"]["path_n_url"])

    @staticmethod
    def test_import_str_static(wrapper_static: SimpleCompBuilder):
        wrapper_static.run(
            "imports", VALID_IMPORTS["avatar"]["static_img"], list_output=True
        )


class TestBadge:
    @pytest.fixture
    def badge(self) -> Badge:
        return Badge(text="Badge")

    @pytest.fixture
    def badge_outline(self) -> Badge:
        return Badge(text="Badge", variant="outline")

    @pytest.fixture
    def wrapper(self, badge: Badge) -> SimpleCompBuilder:
        return SimpleCompBuilder(badge, COMPONENT_DETAILS_DICT["Badge"])

    @pytest.fixture
    def wrapper_outline(self, badge_outline: Badge) -> SimpleCompBuilder:
        return SimpleCompBuilder(badge_outline, COMPONENT_DETAILS_DICT["Badge"])

    @staticmethod
    def test_content_str(wrapper: SimpleCompBuilder):
        wrapper.run("content", VALID_VALS_MAP["badge"]["content"]["simple"])

    @staticmethod
    def test_content_str_outline(wrapper_outline: SimpleCompBuilder):
        wrapper_outline.run("content", VALID_VALS_MAP["badge"]["content"]["variant"])

    @staticmethod
    def test_import_str(wrapper: SimpleCompBuilder):
        wrapper.run("imports", VALID_IMPORTS["badge"])


class TestAccordion:
    @pytest.fixture
    def accordion_simple(self) -> Accordion:
        return Accordion(
            items=[
                AccordionItem(
                    title="Is it accessible?",
                    content="Yes. It adheres to the WAI-ARIA design pattern.",
                ),
                AccordionItem(
                    title="Is it styled?",
                    content="Yes. It comes with default styles that matches the other components' aesthetic.",
                ),
                AccordionItem(
                    title="Is it animated?",
                    content="Yes. It's animated by default, but you can disable it if you prefer.",
                ),
                AccordionItem(
                    title="Can I access it?", content="Not today.", disabled=True
                ),
            ]
        )

    @pytest.fixture
    def accordion_full(self) -> Accordion:
        return Accordion(
            items=[AccordionItem(title="Can I access it?", content="Not today.")],
            type="multiple",
            orientation="horizontal",
            disabled=True,
            styles=None,
        )

    @pytest.fixture
    def wrapper_simple(self, accordion_simple: Accordion) -> SimpleCompBuilder:
        return SimpleCompBuilder(accordion_simple, COMPONENT_DETAILS_DICT["Accordion"])

    @pytest.fixture
    def wrapper_full(self, accordion_full: Accordion) -> SimpleCompBuilder:
        return SimpleCompBuilder(accordion_full, COMPONENT_DETAILS_DICT["Accordion"])

    @staticmethod
    def test_content_str_simple(wrapper_simple: SimpleCompBuilder):
        wrapper_simple.run("content", VALID_VALS_MAP["accordion"]["content"]["simple"])

    @staticmethod
    def test_content_str_full(wrapper_full: SimpleCompBuilder):
        wrapper_full.run("content", VALID_VALS_MAP["accordion"]["content"]["full"])

    @staticmethod
    def test_import_str_simple(wrapper_simple: SimpleCompBuilder):
        wrapper_simple.run("imports", VALID_IMPORTS["accordion"])


class TestAspectRatio:
    @pytest.fixture
    def aspect_ratio_simple(self) -> AspectRatio:
        return AspectRatio(
            img=Image(
                src="./profile.png", alt="Image", styles="rounded-md object-cover"
            ),
            ratio=1,
        )

    @pytest.fixture
    def aspect_ratio_eq_ratio(self) -> AspectRatio:
        return AspectRatio(
            img=Image(
                src="https://example.com/",
                alt="Photo by me",
                styles="rounded-md object-cover",
                fill=True,
            ),
            ratio="16 / 9",
            styles="bg-muted",
        )

    @pytest.fixture
    def wrapper_simple(self, aspect_ratio_simple: AspectRatio) -> SimpleCompBuilder:
        return SimpleCompBuilder(
            aspect_ratio_simple, COMPONENT_DETAILS_DICT["AspectRatio"]
        )

    @pytest.fixture
    def wrapper_eq_ratio(self, aspect_ratio_eq_ratio: AspectRatio) -> SimpleCompBuilder:
        return SimpleCompBuilder(
            aspect_ratio_eq_ratio, COMPONENT_DETAILS_DICT["AspectRatio"]
        )

    @pytest.fixture
    def wrapper_fail_check(
        self, aspect_ratio_fail_check: AspectRatio
    ) -> SimpleCompBuilder:
        return SimpleCompBuilder(
            aspect_ratio_fail_check, COMPONENT_DETAILS_DICT["AspectRatio"]
        )

    @staticmethod
    def test_content_str_simple(wrapper_simple: SimpleCompBuilder):
        wrapper_simple.run(
            "content", VALID_VALS_MAP["aspect_ratio"]["content"]["simple"]
        )

    @staticmethod
    def test_content_str_eq_ratio(wrapper_eq_ratio: SimpleCompBuilder):
        wrapper_eq_ratio.run(
            "content", VALID_VALS_MAP["aspect_ratio"]["content"]["eq_ratio"]
        )

    @staticmethod
    def test_content_str_fail_check():
        with pytest.raises(ValidationError):
            return AspectRatio(
                img=Image(src="$.test", alt="Image", styles="rounded-md object-cover"),
                ratio="16 + test9",
            )

    @staticmethod
    def test_import_str_simple(wrapper_simple: SimpleCompBuilder):
        wrapper_simple.run("imports", VALID_IMPORTS["aspect_ratio"], list_output=True)


class TestProgress:
    @pytest.fixture
    def progress_simple(self) -> Progress:
        return Progress()

    @pytest.fixture
    def progress_custom(self) -> Progress:
        return Progress(value=66, max=500, styles="w-full")

    @pytest.fixture
    def wrapper_simple(self, progress_simple: Progress) -> SimpleCompBuilder:
        return SimpleCompBuilder(progress_simple, COMPONENT_DETAILS_DICT["Progress"])

    @pytest.fixture
    def wrapper_custom(self, progress_custom: Progress) -> SimpleCompBuilder:
        return SimpleCompBuilder(progress_custom, COMPONENT_DETAILS_DICT["Progress"])

    @staticmethod
    def test_content_str_simple(wrapper_simple: SimpleCompBuilder):
        wrapper_simple.run("content", VALID_VALS_MAP["progress"]["content"]["simple"])

    @staticmethod
    def test_content_str_custom(wrapper_custom: SimpleCompBuilder):
        wrapper_custom.run("content", VALID_VALS_MAP["progress"]["content"]["custom"])

    @staticmethod
    def test_logic_str_simple(wrapper_simple: SimpleCompBuilder):
        wrapper_simple.run("logic", VALID_VALS_MAP["progress"]["logic"]["simple"])

    @staticmethod
    def test_logic_str_custom(wrapper_custom: SimpleCompBuilder):
        wrapper_custom.run("logic", VALID_VALS_MAP["progress"]["logic"]["custom"])

    @staticmethod
    def test_import_str_simple(wrapper_simple: SimpleCompBuilder):
        wrapper_simple.run("imports", VALID_IMPORTS["progress"]["simple"])

    @staticmethod
    def test_import_str_custom(wrapper_custom: SimpleCompBuilder):
        wrapper_custom.run("imports", VALID_IMPORTS["progress"]["custom"])


class TestSkeleton:
    @pytest.fixture
    def skeleton_simple_custom(self) -> Skeleton:
        return Skeleton(
            preset="custom",
            styles="flex items-center",
            items=SkeletonShell(styles="h-[125px] w-[250px] rounded-xl"),
        )

    @pytest.fixture
    def skeleton_advanced_custom(self) -> Skeleton:
        return Skeleton(
            preset="custom",
            styles="flex items-center",
            items=[
                SkeletonShell(styles="h-4 w-4"),
                SkeletonGroup(
                    styles="flex flex-col",
                    items=[
                        SkeletonShell(styles="h-4 w-4"),
                        SkeletonShell(styles="h-4 w-4"),
                    ],
                ),
            ],
        )

    @pytest.fixture
    def skeleton_testimonial(self) -> Skeleton:
        return Skeleton(preset="testimonial")

    @pytest.fixture
    def skeleton_card(self) -> Skeleton:
        return Skeleton(preset="card")

    @pytest.fixture
    def wrapper_simple_custom(
        self, skeleton_simple_custom: Skeleton
    ) -> SimpleCompBuilder:
        return SimpleCompBuilder(
            skeleton_simple_custom, COMPONENT_DETAILS_DICT["Skeleton"]
        )

    @pytest.fixture
    def wrapper_advanced_custom(
        self, skeleton_advanced_custom: Skeleton
    ) -> SimpleCompBuilder:
        return SimpleCompBuilder(
            skeleton_advanced_custom, COMPONENT_DETAILS_DICT["Skeleton"]
        )

    @pytest.fixture
    def wrapper_testimonial(self, skeleton_testimonial: Skeleton) -> SimpleCompBuilder:
        return SimpleCompBuilder(
            skeleton_testimonial, COMPONENT_DETAILS_DICT["Skeleton"]
        )

    @pytest.fixture
    def wrapper_card(self, skeleton_card: Skeleton) -> SimpleCompBuilder:
        return SimpleCompBuilder(skeleton_card, COMPONENT_DETAILS_DICT["Skeleton"])

    @staticmethod
    def test_content_str_simple_custom(wrapper_simple_custom: SimpleCompBuilder):
        wrapper_simple_custom.run(
            "content", VALID_VALS_MAP["skeleton"]["content"]["simple_custom"]
        )

    @staticmethod
    def test_content_str_advanced_custom(wrapper_advanced_custom: SimpleCompBuilder):
        wrapper_advanced_custom.run(
            "content", VALID_VALS_MAP["skeleton"]["content"]["advanced_custom"]
        )

    @staticmethod
    def test_content_str_testimonial(wrapper_testimonial: SimpleCompBuilder):
        wrapper_testimonial.run(
            "content", VALID_VALS_MAP["skeleton"]["content"]["testimonial"]
        )

    @staticmethod
    def test_content_str_card(wrapper_card: SimpleCompBuilder):
        wrapper_card.run("content", VALID_VALS_MAP["skeleton"]["content"]["card"])

    @staticmethod
    def test_items_error_without_custom():
        with pytest.raises(ValidationError):
            Skeleton(preset="card", items=SkeletonShell(styles="w-full"))

    @staticmethod
    def test_custom_error_without_items():
        with pytest.raises(ValidationError):
            Skeleton(preset="custom")

    @staticmethod
    def test_import_str(wrapper_simple_custom: SimpleCompBuilder):
        wrapper_simple_custom.run("imports", VALID_IMPORTS["skeleton"])


class TestTable:
    @pytest.fixture
    def table_text(self) -> Table:
        return Table(
            headings=[
                TableCell(text="Invoice", styles="w-[100px]"),
                "Status",
                "Method",
                TableCell(text="Amount", styles="text-right"),
            ],
            body=[
                TableRow(
                    cells=[
                        TableCell(text="INV001", styles="font-medium"),
                        "Paid",
                        "Credit Card",
                        TableCell(text="$250.00", styles="text-right"),
                    ],
                    key="INV001",
                ),
                TableRow(
                    cells=[
                        TableCell(text="INV002", styles="font-medium"),
                        "Pending",
                        "PayPal",
                        TableCell(text="$150.00", styles="text-right"),
                    ],
                    key="INV002",
                ),
            ],
            footer=[
                TableCell(text="Total", col_span=3),
                TableCell(text="$2,500.00", styles="text-right"),
            ],
            caption="A list of your recent invoices.",
        )

    @pytest.fixture
    def table_map(self) -> Table:
        return Table(
            headings=[
                TableCell(text="Invoice", styles="w-[100px]"),
                "Status",
                "Method",
                TableCell(text="Amount", styles="text-right"),
            ],
            body=TableMap(
                obj_name="invoices",
                param_name="invoice",
                row=TableMapRow(
                    cells=[
                        TableCell(text="invoice", styles="font-medium"),
                        "paymentStatus",
                        "paymentMethod",
                        TableCell(text="totalAmount", styles="text-right"),
                    ],
                    key="invoice",
                ),
                map_idx=False,
            ),
            footer=[
                TableCell(text="Total", col_span=3),
                TableCell(text="$2,500.00", styles="text-right"),
            ],
        )

    @pytest.fixture
    def table_map_idx_prefix(self) -> Table:
        return Table(
            headings=[
                TableCell(text="Invoice", styles="w-[100px]"),
                "Status",
                "Method",
                TableCell(text="Amount", styles="text-right"),
            ],
            body=TableMap(
                obj_name="invoices",
                param_name="invoice",
                row=TableMapRow(
                    cells=[
                        TableCell(text="invoice", styles="font-medium"),
                        "$.invoice.paymentStatus",
                        "$.invoice.paymentMethod.payment",
                        TableCell(text="totalAmount", styles="text-right"),
                    ]
                ),
                map_idx=True,
            ),
            footer=[
                TableCell(text="Total", col_span=3),
                TableCell(text="$2,500.00", styles="text-right"),
            ],
            caption="A list of your recent invoices.",
        )

    @pytest.fixture
    def wrapper_text(self, table_text: Table) -> SimpleCompBuilder:
        return SimpleCompBuilder(table_text, COMPONENT_DETAILS_DICT["Table"])

    @pytest.fixture
    def wrapper_map(self, table_map: Table) -> SimpleCompBuilder:
        return SimpleCompBuilder(table_map, COMPONENT_DETAILS_DICT["Table"])

    @pytest.fixture
    def wrapper_map_idx_prefix(self, table_map_idx_prefix: Table) -> SimpleCompBuilder:
        return SimpleCompBuilder(table_map_idx_prefix, COMPONENT_DETAILS_DICT["Table"])

    @staticmethod
    def test_content_str_text(wrapper_text: SimpleCompBuilder):
        wrapper_text.run("content", VALID_VALS_MAP["table"]["content"]["text"])

    @staticmethod
    def test_content_str_map(wrapper_map: SimpleCompBuilder):
        wrapper_map.run("content", VALID_VALS_MAP["table"]["content"]["map"])

    @staticmethod
    def test_content_str_map_idx_prefix(wrapper_map_idx_prefix: SimpleCompBuilder):
        wrapper_map_idx_prefix.run(
            "content", VALID_VALS_MAP["table"]["content"]["map_idx_prefix"]
        )

    @staticmethod
    def test_import_str_text(wrapper_text: SimpleCompBuilder):
        wrapper_text.run("imports", VALID_IMPORTS["table"]["text"])

    @staticmethod
    def test_import_str_map(wrapper_map: SimpleCompBuilder):
        wrapper_map.run("imports", VALID_IMPORTS["table"]["map"])

    @staticmethod
    def test_map_error_str():
        with pytest.raises(ValidationError):
            Table(
                headings=["Status"],
                body=TableMap(
                    obj_name="invoices",
                    param_name="invoice",
                    row=TableMapRow(cells=["$.invoice.paymentStatus test"]),
                ),
                footer=["Total"],
                caption="A list of your recent invoices.",
            )

    @staticmethod
    def test_map_error_table_cell_text():
        with pytest.raises(ValidationError):
            Table(
                headings=["Status"],
                body=TableMap(
                    obj_name="invoices",
                    param_name="invoice",
                    row=TableMapRow(
                        cells=[TableCell(text="invoice test", styles="font-medium")]
                    ),
                ),
                footer=["Total"],
                caption="A list of your recent invoices.",
            )
