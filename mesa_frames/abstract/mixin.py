from abc import ABC, abstractmethod
from collections.abc import Collection, Iterator, Sequence
from copy import copy, deepcopy
from typing import Literal

from typing_extensions import Any, Self

from mesa_frames.types_ import BoolSeries, DataFrame, MaskLike, Series


class CopyMixin(ABC):
    """A mixin class that provides a fast copy method for the class that inherits it.

    Attributes
    ----------
    _copy_with_method : dict[str, tuple[str, list[str]]]
        A dictionary that maps the attribute name to a tuple containing the method name and the arguments to be passed to the method. This is used to copy attributes that use a specific method to be called for copying (eg pd.DataFrame.copy() method).
    _copy_only_reference : list[str]
        A list of attribute names that should only be copied by reference.

    Methods
    -------
    copy(deep: bool = False, memo: dict | None = None) -> Self
        Create a copy of the object. If deep is True, a deep copy is created. If deep is False, a shallow copy is created.


    Returns
    -------
    _type_
        _description_
    """

    _copy_with_method: dict[str, tuple[str, list[str]]] = {}
    _copy_only_reference: list[str] = [
        "_model",
    ]

    @abstractmethod
    def __init__(self): ...

    def copy(
        self,
        deep: bool = False,
        memo: dict | None = None,
        skip: list[str] | None = None,
    ) -> Self:
        """Create a copy of the Class.

        Parameters
        ----------
        deep : bool, optional
            Flag indicating whether to perform a deep copy of the AgentContainer.
            If True, all attributes of the AgentContainer will be recursively copied (except attributes in self._copy_reference_only).
            If False, only the top-level attributes will be copied.
            Defaults to False.
        memo : dict | None, optional
            A dictionary used to track already copied objects during deep copy.
            Defaults to None.
        skip : list[str] | None, optional
            A list of attribute names to skip during the copy process.
            Defaults to None.

        Returns
        -------
        Self
            A new instance of the AgentContainer class that is a copy of the original instance.
        """
        cls = self.__class__
        obj = cls.__new__(cls)

        if skip is None:
            skip = []

        if deep:
            if not memo:
                memo = {}
            memo[id(self)] = obj
            attributes = self.__dict__.copy()
            [
                setattr(obj, k, deepcopy(v, memo))
                for k, v in attributes.items()
                if k not in self._copy_with_method
                and k not in self._copy_only_reference
                and k not in skip
            ]
        else:
            [
                setattr(obj, k, copy(v))
                for k, v in self.__dict__.items()
                if k not in self._copy_with_method
                and k not in self._copy_only_reference
                and k not in skip
            ]

        # Copy attributes with a reference only
        for attr in self._copy_only_reference:
            setattr(obj, attr, getattr(self, attr))

        # Copy attributes with a specified method
        for attr in self._copy_with_method:
            attr_obj = getattr(self, attr)
            attr_copy_method, attr_copy_args = self._copy_with_method[attr]
            setattr(obj, attr, getattr(attr_obj, attr_copy_method)(*attr_copy_args))

        return obj

    def _get_obj(self, inplace: bool) -> Self:
        """Get the object to perform operations on.

        Parameters
        ----------
        inplace : bool
            If inplace, return self. Otherwise, return a copy.

        Returns
        ----------
        Self
            The object to perform operations on.
        """
        if inplace:
            return self
        else:
            return deepcopy(self)

    def __copy__(self) -> Self:
        """Create a shallow copy of the AgentContainer.

        Returns
        -------
        Self
            A shallow copy of the AgentContainer.
        """
        return self.copy(deep=False)

    def __deepcopy__(self, memo: dict) -> Self:
        """Create a deep copy of the AgentContainer.

        Parameters
        ----------
        memo : dict
            A dictionary to store the copied objects.

        Returns
        -------
        Self
            A deep copy of the AgentContainer.
        """
        return self.copy(deep=True, memo=memo)


class DataFrameMixin(ABC):
    @abstractmethod
    def _df_with_columns(
        self, original_df: DataFrame, new_columns: list[str], data: Any
    ) -> DataFrame: ...

    @abstractmethod
    def _df_column_names(self, df: DataFrame) -> list[str]: ...

    @abstractmethod
    def _df_combine_first(
        self, original_df: DataFrame, new_df: DataFrame, index_cols: list[str]
    ) -> DataFrame: ...

    @abstractmethod
    def _df_concat(
        self,
        dfs: Collection[DataFrame],
        how: Literal["horizontal"] | Literal["vertical"] = "vertical",
        ignore_index: bool = False,
    ) -> DataFrame: ...

    @abstractmethod
    def _df_contains(
        self,
        df: DataFrame,
        column: str,
        values: Any | Sequence[Any],
    ) -> BoolSeries: ...

    @abstractmethod
    def _df_constructor(
        self,
        data: Sequence[Sequence] | dict[str | Any] | None = None,
        columns: list[str] | None = None,
        index_col: str | list[str] | None = None,
        dtypes: dict[str, Any] | None = None,
    ) -> DataFrame: ...

    @abstractmethod
    def _df_get_bool_mask(
        self,
        df: DataFrame,
        index_col: str,
        mask: MaskLike | None = None,
        negate: bool = False,
    ) -> BoolSeries: ...

    @abstractmethod
    def _df_get_masked_df(
        self,
        df: DataFrame,
        index_col: str,
        mask: MaskLike | None = None,
        columns: list[str] | None = None,
        negate: bool = False,
    ) -> DataFrame: ...

    @abstractmethod
    def _df_iterator(self, df: DataFrame) -> Iterator[dict[str, Any]]: ...

    @abstractmethod
    def _df_join(
        self,
        left: DataFrame,
        right: DataFrame,
        on: str | list[str] | None = None,
        left_on: str | list[str] | None = None,
        right_on: str | list[str] | None = None,
        how: Literal["left"]
        | Literal["right"]
        | Literal["inner"]
        | Literal["outer"] = "left",
        suffix="_right",
    ) -> DataFrame: ...

    @abstractmethod
    def _df_norm(self, df: DataFrame) -> DataFrame: ...

    @abstractmethod
    def _df_remove(
        self, df: DataFrame, ids: Sequence[Any], index_col: str | None = None
    ) -> DataFrame: ...

    @abstractmethod
    def _df_sample(
        self,
        df: DataFrame,
        n: int | None = None,
        frac: float | None = None,
        with_replacement: bool = False,
        shuffle: bool = False,
        seed: int | None = None,
    ) -> DataFrame: ...

    @abstractmethod
    def _srs_constructor(
        self,
        data: Sequence[Any] | None = None,
        name: str | None = None,
        dtype: Any | None = None,
        index: Sequence[Any] | None = None,
    ) -> Series: ...

    @abstractmethod
    def _srs_contains(
        self,
        srs: Sequence[Any],
        values: Any | Sequence[Any],
    ) -> BoolSeries: ...

    @abstractmethod
    def _srs_range(self, name: str, start: int, end: int, step: int = 1) -> Series: ...
