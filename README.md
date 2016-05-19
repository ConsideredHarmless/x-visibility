# x-visibility
A prototype describing a solution to
https://github.com/phramework/validate/issues/19.

## Implementation

### Special forms
* <code>["quote", <i>expr</i>]</code>

    Evaluates as <code><i>expr</i></code>.

    Example:
```
>>> ["quote", ["not", true]]
["not", true]
>>> ["not", true]
false
>>> ["quote", [1, 2, 3]]
[1, 2, 3]
>>> [1, 2, 3]
error: 1 is not a procedure
```

* <code>["prop", <i>property-name</i>]</code>

    Returns the value of the property with name <code><i>property-name</i></code>.

    Example:

    With JSON property values as `{"x": "b", "y": 3}`:
```
>>> ["prop", "x"]
"b"
>>> ["prop", "y"]
3
>>> ["prop", "z"]
error: no such property
```

### Procedures
* <code>["not", <i>expr</i>]</code>

    Returns the boolean negation of <code><i>expr</i></code>.

* <code>["and", <i>exprs*</i>]</code>

    Returns `true` if every expression in <code><i>exprs*</i></code> evaluates to
`true`.

    Example:
```
>>> ["and", ["not", true], true]
false
>>> ["and", ["not", false]]
true
>>> ["and"]
true
```
* <code>["or", <i>exprs*</i>]</code>

    Returns `true` if at least on expression in <code><i>exprs*</i></code>
evaluates to `true`.

* <code>["member", <i>val</i>, <i>vals</i>]</code>

    ...

    Types:
    * <p><code><i>val</i></code>: value
    * <p><code><i>vals</i></code>: list

    Example:
```
>>> ["member", 3, ["quote", [1, 2, 3]]]
true
>>> ["member", ["quote", "x"], ["quote", ["x", "y"]]]
true
>>> ["member", ["quote", "x"], ["quote", ["a", "b"]]]
false
```

* <code>["in_range", <i>val</i>, <i>vals</i>]</code>

    To be implemented

Notes:

* JSON boolean literals are interpreted as LISP boolean literals.
* `"and"` and `"or"` are special forms in the actual LISP specification, to
allow shortcircuiting. Here, they are implemented as regular procedures.
* <code><i>exprs*</i></code> stands for a sequence of 0 or more expressions.


### Types
Native JSON types lack the ability to distinguish between LISP symbols and
strings. Therefore, to signify that a JSON string is to be interpreted as a
LISP string instead of a symbol, `quote` it.
