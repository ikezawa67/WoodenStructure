"""木構造モジュール"""

from __future__ import annotations

from enum import Enum, auto
from typing import Any, Generator, Generic, Iterable, Iterator, TypeVar

try:
    from graphviz import Digraph
    DRAPHICS_AVAILABLE = True
except ImportError:
    DRAPHICS_AVAILABLE = False

_T = TypeVar('_T')


class TraverseType(Enum):
    """走査法の列挙型クラス
    """
    PRE_ORDER = auto()  # 深さ優先探索 (行きがけ順)
    IN_ORDER = auto()  # 深さ優先探索 (通りがけ順)
    POST_ORDER = auto()  # 深さ優先探索 (帰りがけ順)
    LEVEL_ORDER = auto()  # 幅優先探索 (レベル順)


class Node(Generic[_T]):
    """二分探索木のノードクラス
    """

    def __init__(self, value: _T, depth: int = 0, left: Node[_T] | None = None, right: Node[_T] | None = None) -> None:
        self.value = value
        self._depth = depth
        self.left = left
        self.right = right

    @property
    def depth(self):
        """ノードの深さを取得するプロパティ

        Returns:
            _type_: ノードの深さ
        """
        return self._depth

    def __repr__(self) -> str:
        return repr(self.value)

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Node):
            return self.value < other.value
        else:
            return self.value < other

    def __le__(self, other: Any) -> bool:
        if isinstance(other, Node):
            return self.value <= other.value
        else:
            return self.value <= other

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Node):
            return self.value == other.value
        else:
            return self.value == other

    def __ne__(self, other: Any) -> bool:
        if isinstance(other, Node):
            return self.value != other.value
        else:
            return self.value != other

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, Node):
            return self.value > other.value
        else:
            return self.value > other

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, Node):
            return self.value >= other.value
        else:
            return self.value >= other


class BinaryTree:
    """二分探索木のクラス
    """

    def __init__(self, iterable: Iterable[_T] | None = None, traverse_type: TraverseType = TraverseType.PRE_ORDER) -> None:
        self.root: Node | None = None
        self.traverse_type = traverse_type
        for i in iterable:
            self.insert(i)

    def __iter__(self) -> Generator[Node | None, None, None]:
        def _pre_order(node: Node | None) -> Generator[Node | None, None, None]:
            if node:
                yield node
                for _node in _pre_order(node.left):
                    yield _node
                for _node in _pre_order(node.right):
                    yield _node

        def _in_order(node: Node | None) -> Generator[Node | None, None, None]:
            if node:
                for _node in _in_order(node.left):
                    yield _node
                yield node
                for _node in _in_order(node.right):
                    yield _node

        def _post_order(node: Node | None) -> Generator[Node | None, None, None]:
            if node:
                for _node in _post_order(node.left):
                    yield _node
                for _node in _post_order(node.right):
                    yield _node
                yield node

        def _level_order(node: Node | None) -> Iterator[Node]:
            def _(node: Node | None, result: dict[int, list[Node]]):
                if node:
                    if node.depth not in result.keys():
                        result[node.depth] = [node]
                    else:
                        result[node.depth].append(node)
                    result = _(node.left, result)
                    result = _(node.right, result)
                return result
            return iter([node for r in _(node, {}).values() for node in r])

        if self.traverse_type == TraverseType.PRE_ORDER:
            return _pre_order(self.root)
        elif self.traverse_type == TraverseType.IN_ORDER:
            return _in_order(self.root)
        elif self.traverse_type == TraverseType.POST_ORDER:
            return _post_order(self.root)
        else:
            return _level_order(self.root)

    def __contains__(self, value: Any) -> bool:
        for _node in self:
            if _node == value:
                return True
        return False

    def insert(self, value: _T) -> None:
        """値を二分探索木に挿入するメソッド

        Args:
            value (_T): 挿入する値
        """
        def _insert(node: Node | None, value: _T, depth) -> Node:
            if node is None:
                return Node(value, depth)
            elif value == node:
                return node
            elif value < node:
                node.left = _insert(node.left, value, depth + 1)
            else:
                node.right = _insert(node.right, value, depth + 1)
            return node
        self.root = _insert(self.root, value, 0)

    def delete(self, value: _T) -> None:
        """値を二分探索木から削除するメソッド

        Args:
            value (_T): 削除する値
        """
        def _search_min(node: Node):
            if node.left is None:
                return node.value
            return _search_min(node.left)

        def _delete_min(node: Node):
            if node.left is None:
                return node.right
            node.left = _delete_min(node.left)
            return node

        def _delete(node: Node | None, value: _T) -> Node | None:
            if node:
                if value == node.value:
                    if node.left is None:
                        return node.right
                    elif node.right is None:
                        return node.left
                    else:
                        node.value = _search_min(node.right)
                        node.right = _delete_min(node.right)
                elif value < node.value:
                    node.left = _delete(node.left, value)
                else:
                    node.right = _delete(node.right, value)
            return node
        self.root = _delete(self.root, value)

    if DRAPHICS_AVAILABLE:
        def view(self) -> None:
            """二分探索木のグラフを描画するメソッド
            """
            graph = Digraph()
            graph.attr('node', shape='circle')
            for node in self:
                if node.left:
                    graph.edge(f'{node.value}', f'{node.left.value}')
                if node.right:
                    graph.edge(f'{node.value}', f'{node.right.value}')
            graph.view()


if __name__ == '__main__':
    tmp = [22, 19, 9, 11, 17, 20, 21, 10, 4, 12, 7, 14,
           24, 23, 16, 6, 13, 3, 5, 8, 2, 0, 1, 15, 18]
    tree = BinaryTree(tmp)
    for node in tree:
        print(node)
    tree.view()
