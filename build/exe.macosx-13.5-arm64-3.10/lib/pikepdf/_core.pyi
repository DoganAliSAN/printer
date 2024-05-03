# SPDX-FileCopyrightText: 2022 James R. Barlow
# SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

# pybind11 does not generate type annotations yet, and mypy doesn't understand
# the way we're augmenting C++ classes with Python methods as in
# pikepdf/_methods.py. Thus, we need to manually spell out the resulting types
# after augmenting.
import datetime
from abc import abstractmethod
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import (
    Any,
    BinaryIO,
    Callable,
    ClassVar,
    Collection,
    Iterable,
    Iterator,
    KeysView,
    Literal,
    Mapping,
    MutableMapping,
    Sequence,
    TypeVar,
    overload,
)

from pikepdf.models.encryption import Encryption, EncryptionInfo, Permissions
from pikepdf.models.image import PdfInlineImage
from pikepdf.models.metadata import PdfMetadata
from pikepdf.models.outlines import Outline
from pikepdf.objects import Array, Dictionary, Name, Stream, String

# This is the whole point of stub files, but apparently we have to do this...
# pylint: disable=no-method-argument,unused-argument,no-self-use,too-many-public-methods

T = TypeVar('T', bound='Object')
Numeric = TypeVar('Numeric', int, float, Decimal)

class Buffer: ...

# Exceptions

class DataDecodingError(Exception): ...
class JobUsageError(Exception): ...
class PasswordError(Exception): ...
class PdfError(Exception): ...
class ForeignObjectError(Exception): ...
class DeletedObjectError(Exception): ...

# Enums
class AccessMode(Enum):
    default: int = ...
    mmap: int = ...
    mmap_only: int = ...
    stream: int = ...

class EncryptionMethod(Enum):
    none: int = ...
    unknown: int = ...
    rc4: int = ...
    aes: int = ...
    aesv3: int = ...

class ObjectStreamMode(Enum):
    disable: int = ...
    generate: int = ...
    preserve: int = ...

class ObjectType(Enum):
    array: int = ...
    boolean: int = ...
    dictionary: int = ...
    inlineimage: int = ...
    integer: int = ...
    name_: int = ...
    null: int = ...
    operator: int = ...
    real: int = ...
    reserved: int = ...
    stream: int = ...
    string: int = ...
    uninitialized: int = ...

class StreamDecodeLevel(Enum):
    all: int = ...
    generalized: int = ...
    none: int = ...
    specialized: int = ...

class TokenType(Enum):
    array_close: int = ...
    array_open: int = ...
    bad: int = ...
    bool: int = ...
    brace_close: int = ...
    brace_open: int = ...
    comment: int = ...
    dict_close: int = ...
    dict_open: int = ...
    eof: int = ...
    inline_image: int = ...
    integer: int = ...
    name_: int = ...
    null: int = ...
    real: int = ...
    space: int = ...
    string: int = ...
    word: int = ...

class Object:
    def _ipython_key_completions_(self) -> KeysView | None: ...
    def _inline_image_raw_bytes(self) -> bytes: ...
    def _parse_page_contents(self, callbacks: Callable) -> None: ...
    def _parse_page_contents_grouped(
        self, whitelist: str
    ) -> list[tuple[Collection[Object | PdfInlineImage], Operator]]: ...
    @staticmethod
    def _parse_stream(stream: Object, parser: StreamParser) -> list: ...
    @staticmethod
    def _parse_stream_grouped(stream: Object, whitelist: str) -> list: ...
    def _repr_mimebundle_(self, include=None, exclude=None) -> dict | None: ...
    def _write(
        self,
        data: bytes,
        filter: Object,  # pylint: disable=redefined-builtin
        decode_parms: Object,
    ) -> None: ...
    def append(self, pyitem: Any) -> None: ...
    def as_dict(self) -> _ObjectMapping: ...
    def as_list(self) -> _ObjectList: ...
    def emplace(self, other: Object, retain: Iterable[Name] = ...) -> None: ...
    def extend(self, arg0: Iterable[Object]) -> None: ...
    @overload
    def get(self, key: str, default: T | None = ...) -> Object | T | None: ...
    @overload
    def get(self, key: Name, default: T | None = ...) -> Object | T | None: ...
    def get_raw_stream_buffer(self) -> Buffer: ...
    def get_stream_buffer(self, decode_level: StreamDecodeLevel = ...) -> Buffer: ...
    def is_owned_by(self, possible_owner: Pdf) -> bool: ...
    def items(self) -> Iterable[tuple[str, Object]]: ...
    def keys(self) -> set[str]: ...
    @staticmethod
    def parse(stream: bytes, description: str = ...) -> Object: ...
    def read_bytes(self, decode_level: StreamDecodeLevel = ...) -> bytes: ...
    def read_raw_bytes(self) -> bytes: ...
    def same_owner_as(self, other: Object) -> bool: ...
    def to_json(self, dereference: bool = ...) -> bytes: ...
    def unparse(self, resolved: bool = ...) -> bytes: ...
    def with_same_owner_as(self, arg0: Object) -> Object: ...
    def wrap_in_array(self) -> Array: ...
    def write(
        self,
        data: bytes,
        *,
        filter: Name | Array | None = ...,  # pylint: disable=redefined-builtin
        decode_parms: Dictionary | Array | None = ...,
        type_check: bool = ...,
    ) -> None: ...
    def __bytes__(self) -> bytes: ...
    @overload
    def __contains__(self, arg0: Object) -> bool: ...
    @overload
    def __contains__(self, arg0: str) -> bool: ...
    def __copy__(self) -> Object: ...
    def __delattr__(self, arg0: str) -> None: ...
    @overload
    def __delitem__(self, arg0: str) -> None: ...
    @overload
    def __delitem__(self, arg0: Object) -> None: ...
    @overload
    def __delitem__(self, arg0: int) -> None: ...
    def __dir__(self) -> list: ...
    def __eq__(self, other: Any) -> bool: ...
    def __getattr__(self, arg0: str) -> Object: ...
    @overload
    def __getitem__(self, arg0: str) -> Object: ...
    @overload
    def __getitem__(self, arg0: Object) -> Object: ...
    @overload
    def __getitem__(self, arg0: int) -> Object: ...
    def __hash__(self) -> int: ...
    def __iter__(self) -> Iterable[Object]: ...
    def __len__(self) -> int: ...
    def __setattr__(self, arg0: str, arg1: object) -> None: ...
    @overload
    def __setitem__(self, arg0: str, arg1: Object) -> None: ...
    @overload
    def __setitem__(self, arg0: Object, arg1: Object) -> None: ...
    @overload
    def __setitem__(self, arg0: str, arg1: object) -> None: ...
    @overload
    def __setitem__(self, arg0: Object, arg1: object) -> None: ...
    @overload
    def __setitem__(self, arg0: int, arg1: Object) -> None: ...
    @overload
    def __setitem__(self, arg0: int, arg1: object) -> None: ...
    @property
    def _objgen(self) -> tuple[int, int]: ...
    @property
    def _type_code(self) -> ObjectType: ...
    @property
    def _type_name(self) -> str: ...
    @property
    def images(self) -> _ObjectMapping: ...
    @property
    def is_indirect(self) -> bool: ...
    @property
    def is_rectangle(self) -> bool: ...
    @property
    def objgen(self) -> tuple[int, int]: ...
    @property
    def stream_dict(self) -> Object: ...
    @stream_dict.setter
    def stream_dict(self, val: Object) -> None: ...

class ObjectHelper:
    def __eq__(self, other: Any) -> bool: ...
    @property
    def obj(self) -> Object: ...

class _ObjectList:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, arg0: _ObjectList) -> None: ...
    @overload
    def __init__(self, arg0: Iterable) -> None: ...
    @overload
    def __init__(*args, **kwargs) -> None: ...
    def append(self, x: Object) -> None: ...
    def clear(self) -> None: ...
    def count(self, x: Object) -> int: ...
    @overload
    def extend(self, L: _ObjectList) -> None: ...
    @overload
    def extend(self, L: Iterable[Object]) -> None: ...
    def insert(self, i: int, x: Object) -> None: ...
    @overload
    def pop(self) -> Object: ...
    @overload
    def pop(self, i: int) -> Object: ...
    @overload
    def pop(*args, **kwargs) -> Any: ...
    def remove(self, x: Object) -> None: ...
    def __bool__(self) -> bool: ...
    def __contains__(self, x: Object) -> bool: ...
    @overload
    def __delitem__(self, arg0: int) -> None: ...
    @overload
    def __delitem__(self, arg0: slice) -> None: ...
    @overload
    def __delitem__(*args, **kwargs) -> Any: ...
    def __eq__(self, other: Any) -> bool: ...
    @overload
    def __getitem__(self, s: slice) -> _ObjectList: ...
    @overload
    def __getitem__(self, arg0: int) -> Object: ...
    @overload
    def __getitem__(*args, **kwargs) -> Any: ...
    def __iter__(self) -> Iterator[Object]: ...
    def __len__(self) -> int: ...
    def __ne__(self, other: Any) -> bool: ...
    @overload
    def __setitem__(self, arg0: int, arg1: Object) -> None: ...
    @overload
    def __setitem__(self, arg0: slice, arg1: _ObjectList) -> None: ...
    @overload
    def __setitem__(*args, **kwargs) -> Any: ...

class _ObjectMapping:
    get: Any = ...
    keys: Any = ...
    values: Any = ...
    def __contains__(self, arg0: Name | str) -> bool: ...
    def __init__(self) -> None: ...
    def items(self) -> Iterator: ...
    def __bool__(self) -> bool: ...
    def __delitem__(self, arg0: str) -> None: ...
    def __getitem__(self, arg0: Name | str) -> Object: ...
    def __iter__(self) -> Iterator: ...
    def __len__(self) -> int: ...
    def __setitem__(self, arg0: str, arg1: Object) -> None: ...

class Operator(Object): ...

class Annotation:
    def __init__(self, arg0: Object) -> None: ...
    @overload
    def get_appearance_stream(self, which: Object) -> Object: ...
    @overload
    def get_appearance_stream(self, which: Object, state: Object) -> Object: ...
    def get_page_content_for_appearance(
        self,
        name: Object,
        rotate: int,
        required_flags: int = ...,
        forbidden_flags: int = ...,
    ) -> bytes: ...
    @property
    def appearance_dict(self) -> Object: ...
    @property
    def appearance_state(self) -> Object: ...
    @property
    def flags(self) -> int: ...
    @property
    def obj(self) -> Object: ...
    @property
    def subtype(self) -> str: ...

class AttachedFile:
    _creation_date: str
    _mod_date: str
    creation_date: datetime.datetime | None
    mime_type: str
    mod_date: datetime.datetime | None
    @property
    def md5(self) -> bytes: ...
    @property
    def obj(self) -> Object: ...
    def read_bytes(self) -> bytes: ...
    @property
    def size(self) -> int: ...

class AttachedFileSpec:
    description: str
    filename: str
    def __init__(
        self,
        data: bytes,
        *,
        description: str,
        filename: str,
        mime_type: str,
        creation_date: str,
        mod_date: str,
    ) -> None: ...
    def get_all_filenames(self) -> dict: ...
    @overload
    def get_file(self) -> AttachedFile: ...
    @overload
    def get_file(self, name: Name) -> AttachedFile: ...
    @property
    def obj(self) -> Object: ...
    @staticmethod
    def from_filepath(
        pdf: Pdf, path: Path | str, *, description: str = ''
    ) -> AttachedFileSpec: ...
    @property
    def relationship(self) -> Name | None: ...
    @relationship.setter
    def relationship(self, value: Name | None) -> None: ...

class Attachments(MutableMapping[str, AttachedFileSpec]):
    def __contains__(self, k: object) -> bool: ...
    def __delitem__(self, k: str) -> None: ...
    def __eq__(self, other: Any) -> bool: ...
    def __getitem__(self, k: str) -> AttachedFileSpec: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def __setitem__(self, k: str, v: AttachedFileSpec): ...
    def __init__(self, *args, **kwargs) -> None: ...
    def _add_replace_filespec(self, arg0: str, arg1: AttachedFileSpec) -> None: ...
    def _get_all_filespecs(self) -> dict[str, AttachedFileSpec]: ...
    def _get_filespec(self, arg0: str) -> AttachedFileSpec: ...
    def _remove_filespec(self, arg0: str) -> bool: ...
    @property
    def _has_embedded_files(self) -> bool: ...

class Token:
    def __init__(self, arg0: TokenType, arg1: bytes) -> None: ...
    def __eq__(self, other: Any) -> bool: ...
    @property
    def error_msg(self) -> str: ...
    @property
    def raw_value(self) -> bytes: ...
    @property
    def type_(self) -> TokenType: ...
    @property
    def value(self) -> str: ...

class _QPDFTokenFilter: ...

class TokenFilter(_QPDFTokenFilter):
    def __init__(self) -> None: ...
    def handle_token(self, token: Token = ...) -> None | list | Token: ...

class StreamParser:
    def __init__(self) -> None: ...
    @abstractmethod
    def handle_eof(self) -> None: ...
    @abstractmethod
    def handle_object(self, obj: Object, offset: int, length: int) -> None: ...

class Page:
    _repr_mimebundle_: Any = ...
    @overload
    def __init__(self, arg0: Object) -> None: ...
    @overload
    def __init__(self, arg0: Page) -> None: ...
    def __contains__(self, key: Any) -> bool: ...
    def __delattr__(self, name: Any) -> None: ...
    def __eq__(self, other: Any) -> bool: ...
    def __getattr__(self, name: Any) -> Object: ...
    def __getitem__(self, name: Any) -> Object: ...
    def __setattr__(self, name: Any, value: Any): ...
    def __setitem__(self, name: Any, value: Any): ...
    def _get_artbox(self, arg0: bool, arg1: bool) -> Object: ...
    def _get_bleedbox(self, arg0: bool, arg1: bool) -> Object: ...
    def _get_cropbox(self, arg0: bool, arg1: bool) -> Object: ...
    def _get_mediabox(self, arg0: bool) -> Object: ...
    def _get_trimbox(self, arg0: bool, arg1: bool) -> Object: ...
    def add_content_token_filter(self, tf: TokenFilter) -> None: ...
    def add_overlay(
        self,
        other: Object | Page,
        rect: Rectangle | None,
        *,
        push_stack: bool | None = ...,
    ): ...
    def add_underlay(self, other: Object | Page, rect: Rectangle | None): ...
    def as_form_xobject(self, handle_transformations: bool = ...) -> Object: ...
    def calc_form_xobject_placement(
        self,
        formx: Object,
        name: Name,
        rec: Rectangle,
        *,
        invert_transformations: bool,
        allow_shrink: bool,
        allow_expand: bool,
    ) -> bytes: ...
    def contents_add(
        self, contents: Stream | bytes, *, prepend: bool = ...
    ) -> None: ...
    def contents_coalesce(self) -> None: ...
    def emplace(self, other: Page, retain: Iterable[Name]) -> None: ...
    def externalize_inline_images(self, min_size: int = ...) -> None: ...
    def get(self, key: str | Name, default: T | None = ...) -> T | None | Object: ...
    def get_filtered_contents(self, tf: TokenFilter) -> bytes: ...
    def index(self) -> int: ...
    def label(self) -> str: ...
    def parse_contents(self, arg0: StreamParser) -> None: ...
    def remove_unreferenced_resources(self) -> None: ...
    def rotate(self, angle: int, relative: bool) -> None: ...
    @property
    def images(self) -> _ObjectMapping: ...
    @property
    def cropbox(self) -> Array: ...
    @cropbox.setter
    def cropbox(self, val: Array) -> None: ...
    @property
    def mediabox(self) -> Array: ...
    @mediabox.setter
    def mediabox(self, val: Array) -> None: ...
    @property
    def obj(self) -> Dictionary: ...
    @property
    def trimbox(self) -> Array: ...
    @trimbox.setter
    def trimbox(self, val: Array) -> None: ...
    @property
    def resources(self) -> Dictionary: ...
    def add_resource(
        self,
        res: Object,
        res_type: Name,
        name: Name | None = None,
        *,
        prefix: str = '',
        replace_existing: bool = True,
    ) -> Name: ...

class PageList:
    def __init__(self, *args, **kwargs) -> None: ...
    def append(self, page: Page) -> None: ...
    @overload
    def extend(self, other: PageList) -> None: ...
    @overload
    def extend(self, iterable: Iterable[Page]) -> None: ...
    def insert(self, index: int, obj: Page) -> None: ...
    def p(self, pnum: int) -> Page: ...
    def remove(self, **kwargs) -> None: ...
    def reverse(self) -> None: ...
    @overload
    def __delitem__(self, arg0: int) -> None: ...
    @overload
    def __delitem__(self, arg0: slice) -> None: ...
    @overload
    def __getitem__(self, arg0: int) -> Page: ...
    @overload
    def __getitem__(self, arg0: slice) -> list[Page]: ...
    def __iter__(self) -> PageList: ...
    def __len__(self) -> int: ...
    def __next__(self) -> Page: ...
    @overload
    def __setitem__(self, arg0: int, arg1: Page) -> None: ...
    @overload
    def __setitem__(self, arg0: slice, arg1: Iterable[Page]) -> None: ...

class Pdf:
    _repr_mimebundle_: Any = ...
    def add_blank_page(self, *, page_size: tuple[Numeric, Numeric] = ...) -> Page: ...
    def __enter__(self) -> Pdf: ...
    def __exit__(self, exc_type, exc_value, traceback) -> None: ...
    def __init__(self, *args, **kwargs) -> None: ...
    def _add_page(self, page: Object, first: bool = ...) -> None: ...
    def _decode_all_streams_and_discard(self) -> None: ...
    def _get_object_id(self, arg0: int, arg1: int) -> Object: ...
    def _process(self, arg0: str, arg1: bytes) -> None: ...
    def _remove_page(self, arg0: Object) -> None: ...
    def _replace_object(self, arg0: tuple[int, int], arg1: Object) -> None: ...
    def _swap_objects(self, arg0: tuple[int, int], arg1: tuple[int, int]) -> None: ...
    def check(self) -> list[str]: ...
    def check_linearization(self, stream: object = ...) -> bool: ...
    def close(self) -> None: ...
    def copy_foreign(self, h: Object) -> Object: ...
    @overload
    def get_object(self, objgen: tuple[int, int]) -> Object: ...
    @overload
    def get_object(self, objid: int, gen: int) -> Object: ...
    def get_warnings(self) -> list: ...
    @overload
    def make_indirect(self, h: T) -> T: ...
    @overload
    def make_indirect(self, obj: Any) -> Object: ...
    def make_stream(self, data: bytes, d=None, **kwargs) -> Stream: ...
    @classmethod
    def new(cls) -> Pdf: ...
    @staticmethod
    def open(
        filename_or_stream: Path | str | BinaryIO,
        *,
        password: str | bytes = "",
        hex_password: bool = False,
        ignore_xref_streams: bool = False,
        suppress_warnings: bool = True,
        attempt_recovery: bool = True,
        inherit_page_attributes: bool = True,
        access_mode: AccessMode = AccessMode.default,
        allow_overwriting_input: bool = False,
    ) -> Pdf: ...
    def open_metadata(
        self,
        set_pikepdf_as_editor: bool = True,
        update_docinfo: bool = True,
        strict: bool = False,
    ) -> PdfMetadata: ...
    def open_outline(self, max_depth: int = 15, strict: bool = False) -> Outline: ...
    def remove_unreferenced_resources(self) -> None: ...
    def save(
        self,
        filename_or_stream: Path | str | BinaryIO | None = None,
        *,
        static_id: bool = False,
        preserve_pdfa: bool = True,
        min_version: str | tuple[str, int] = "",
        force_version: str | tuple[str, int] = "",
        fix_metadata_version: bool = True,
        compress_streams: bool = True,
        stream_decode_level: StreamDecodeLevel | None = None,
        object_stream_mode: ObjectStreamMode = ObjectStreamMode.preserve,
        normalize_content: bool = False,
        linearize: bool = False,
        qdf: bool = False,
        progress: Callable[[int], None] | None = None,
        encryption: Encryption | bool | None = None,
        recompress_flate: bool = False,
        deterministic_id: bool = False,
    ) -> None: ...
    def show_xref_table(self) -> None: ...
    @property
    def Root(self) -> Object: ...
    @property
    def _allow_accessibility(self) -> bool: ...
    @property
    def _allow_extract(self) -> bool: ...
    @property
    def _allow_modify_all(self) -> bool: ...
    @property
    def _allow_modify_annotation(self) -> bool: ...
    @property
    def _allow_modify_assembly(self) -> bool: ...
    @property
    def _allow_modify_form(self) -> bool: ...
    @property
    def _allow_modify_other(self) -> bool: ...
    @property
    def _allow_print_highres(self) -> bool: ...
    @property
    def _allow_print_lowres(self) -> bool: ...
    @property
    def _encryption_data(self) -> dict: ...
    @property
    def _pages(self) -> Any: ...
    @property
    def allow(self) -> Permissions: ...
    @property
    def docinfo(self) -> Object: ...
    @docinfo.setter
    def docinfo(self, val: Object) -> None: ...
    @property
    def encryption(self) -> EncryptionInfo: ...
    @property
    def extension_level(self) -> int: ...
    @property
    def filename(self) -> str: ...
    @property
    def is_encrypted(self) -> bool: ...
    @property
    def is_linearized(self) -> bool: ...
    @property
    def objects(self) -> Any: ...
    @property
    def pages(self) -> PageList: ...
    @property
    def pdf_version(self) -> str: ...
    @property
    def root(self) -> Object: ...
    @property
    def trailer(self) -> Object: ...
    @property
    def user_password_matched(self) -> bool: ...
    @property
    def owner_password_matched(self) -> bool: ...
    def generate_appearance_streams(self) -> None: ...
    def flatten_annotations(self, mode: str) -> None: ...
    @property
    def attachments(self) -> Attachments: ...

class Rectangle:
    llx: float = ...
    lly: float = ...
    urx: float = ...
    ury: float = ...
    @overload
    def __init__(self, llx: float, lly: float, urx: float, ury: float) -> None: ...
    @overload
    def __init__(self, a: Array) -> None: ...
    @property
    def width(self) -> float: ...
    @property
    def height(self) -> float: ...
    @property
    def lower_left(self) -> tuple[float, float]: ...
    @property
    def lower_right(self) -> tuple[float, float]: ...
    @property
    def upper_left(self) -> tuple[float, float]: ...
    @property
    def upper_right(self) -> tuple[float, float]: ...
    def as_array(self) -> Array: ...

class NameTree(MutableMapping[str | bytes, Object]):
    @staticmethod
    def new(pdf: Pdf, auto_repair: bool = True) -> NameTree: ...
    def __contains__(self, name: object) -> bool: ...
    def __delitem__(self, name: str | bytes) -> None: ...
    def __eq__(self, other: Any) -> bool: ...
    def __getitem__(self, name: str | bytes) -> Object: ...
    def __iter__(self) -> Iterator[bytes]: ...
    def __len__(self) -> int: ...
    def __setitem__(self, name: str | bytes, o: Object) -> None: ...
    def __init__(self, obj: Object, *, auto_repair: bool = ...) -> None: ...
    def _as_map(self) -> _ObjectMapping: ...
    @property
    def obj(self) -> Object: ...

class NumberTree(MutableMapping[int, Object]):
    @staticmethod
    def new(pdf: Pdf, auto_repair: bool = True) -> NumberTree: ...
    def __contains__(self, key: object) -> bool: ...
    def __delitem__(self, key: int) -> None: ...
    def __eq__(self, other: Any) -> bool: ...
    def __getitem__(self, key: int) -> Object: ...
    def __iter__(self) -> Iterator[int]: ...
    def __len__(self) -> int: ...
    def __setitem__(self, key: int, o: Object) -> None: ...
    def __init__(self, obj: Object, *, auto_repair: bool = ...) -> None: ...
    def _as_map(self) -> _ObjectMapping: ...
    @property
    def obj(self) -> Object: ...

class ContentStreamInstruction:
    @property
    def operands(self) -> _ObjectList: ...
    @property
    def operator(self) -> Operator: ...
    def __getitem__(self, index: int) -> _ObjectList | Operator: ...
    def __len__(self) -> int: ...

class ContentStreamInlineImage:
    @property
    def operands(self) -> _ObjectList: ...
    @property
    def operator(self) -> Operator: ...
    def __getitem__(self, index: int) -> _ObjectList | Operator: ...
    def __len__(self) -> int: ...
    @property
    def iimage(self) -> PdfInlineImage: ...

class Job:
    EXIT_ERROR: ClassVar[int] = 2
    EXIT_WARNING: ClassVar[int] = 3
    EXIT_IS_NOT_ENCRYPTED: ClassVar[int] = 2
    EXIT_CORRECT_PASSWORD: ClassVar[int] = 3
    LATEST_JOB_JSON: ClassVar[int]
    LATEST_JSON: ClassVar[int]

    @staticmethod
    def json_out_schema(*, schema: int) -> str: ...
    @staticmethod
    def job_json_schema(*, schema: int) -> str: ...
    @overload
    def __init__(self, json: str) -> None: ...
    @overload
    def __init__(self, json_dict: Mapping) -> None: ...
    @overload
    def __init__(
        self, args: Sequence[str | bytes], *, progname: str = "pikepdf"
    ) -> None: ...
    def check_configuration(self) -> None: ...
    @property
    def creates_output(self) -> bool: ...
    @property
    def message_prefix(self) -> str: ...
    def run(self) -> None: ...
    @property
    def has_warnings(self) -> bool: ...
    @property
    def exit_code(self) -> int: ...
    @property
    def encryption_status(self) -> dict[str, bool]: ...

def _Null() -> Any: ...
def _encode(handle: Any) -> Object: ...
def _new_array(arg0: Iterable) -> Array: ...
def _new_boolean(arg0: bool) -> Object: ...
def _new_dictionary(arg0: Mapping[Any, Any]) -> Dictionary: ...
def _new_integer(arg0: int) -> Object: ...
def _new_name(arg0: str) -> Name: ...
def _new_operator(op: str) -> Operator: ...
@overload
def _new_real(arg0: str) -> Object: ...
@overload
def _new_real(value: float, places: int = ...) -> Object: ...
def _new_stream(arg0: Pdf, arg1: bytes) -> Stream: ...
def _new_string(s: str | bytes) -> String: ...
def _new_string_utf8(s: str) -> String: ...
def _test_file_not_found(*args, **kwargs) -> Any: ...
def _translate_qpdf_logic_error(arg0: str) -> str: ...
def get_decimal_precision() -> int: ...
def pdf_doc_to_utf8(pdfdoc: bytes) -> str: ...
def qpdf_version() -> str: ...
def set_access_default_mmap(mmap: bool) -> bool: ...
def get_access_default_mmap() -> bool: ...
def set_decimal_precision(prec: int) -> int: ...
def unparse(obj: Any) -> bytes: ...
def utf8_to_pdf_doc(utf8: str, unknown: bytes) -> tuple[bool, bytes]: ...
def _unparse_content_stream(contentstream: Iterable[Any]) -> bytes: ...
def set_flate_compression_level(
    level: Literal[-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
) -> int: ...
