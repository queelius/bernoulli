@page noisy_logic Noisy Logic

## Noisy Turing machines: noisy logic gates

As we consider more complex compound data types, which may always be modeled as
functions, we will see that there are many ways these types can participate
in the Bernoulli Boolean model. When a Bernoulli value is introduced into the
computational model, the entire computation outputs a final result that is
a Bernoulli type, e.g., `bernoulli<pair<T1,T2>>`, `pair<T1,bernoulli<T2>`, and so
on.

The easiest way to think about this is to just consider a Universal Turing machine
in which we build programs by composing circuits of binary logic-gates, like `and`,
`or`, and `not`. In general, if we replace a single input into the circuit with a
Bernoulli Boolean, the output of the circuit is a one or more Bernoulli Booleans.
Moreover, and more interestingly, we can replace some of the logic gates with
noisy logic-gates, or Bernoulli logic-gates, and the output of the circuit is
also a Bernoulli Boolean. We can always discard information about the uncertainty
in the output of the circuit, and just get Boolean, but if the uncertainty is
non-negligible, then we may want to keep track of it.

So, let's consider the set of binary functions
`f : (bool, bool) -> bool`. 

There are 2^2 = 4 possible functions `f : bool -> bool` since for each possible
input, $1$ or $0$, we have two possible outputs, $1$ or $0$.

> More generally, if we have `f : X -> Y`, then we have `|Y|^|X|` possible functions,
> where `|.|` denotes the cardinality of a set. For instance, if `X = (bool, bool)`
> and `Y = bool`, then we have `2^4 = 16` possible functions, since `|X| = 4` and `|Y| = 2`.

Each of these functions has a designated name, which we can use to refer to them,
like `and`, `xor`, etc. However, we are just going to look at `and`.

Table 4: `and : (bool, bool) -> bool`

| `x1` | `x2` | `and(x1, x2)` |
|------|------|---------------|
| true | true | true          |
| true | false| false         |
| false| true | false         |
| false| false| false         |

Now, let's consider
```cpp
and : (bernoulli<bool,1>, bernoulli<bool,1>) -> bernoulli<bool,2>`
```

This is more complicated than might first seem. An error occurs if
`and` returns $1$ when it should return $0$, or vice versa. The input
variables represent *latent* values, so they do not have a definite value.

We will go row by row, and examine the probability that the output is correct for
each *output*.

### Case 1: The Correct Output Is True

In order for the output to be true, both noisy inputs must be true, which is just
the product of the probabilities of each condition being true since they are
statistically independent outcomes. 

### Case 2: The Correct Output Is False Given `x1 = true` and `x2 = false`

Consider `and(bernoulli<bool,1>{true}, bernoulli<bool,1>{false})`.
For this to be true, the first must be a true positive and the second must be
a false postive, which is just `p1 * (1-p2)`. Since we are interested in the probability that it correctly maps to false, that is just
`1 - p1 * (1-p2) = 1 - p1 + p1 * p2`.

### Case 3: The Correct Output Is False Given `x1 = false` and `x2 = true`

Consider `and(bernoulli<bool,1>{false}, bernoulli<bool,1>{true})`.
For this to be true, the first must be a false positive and the second must
be a true positive, which is just `(1-p1) * p2`. Since we are interested in the
probability that it maps correctly to false, that is just
`1 - (1-p1) * p2 = 1 - p2 + p1 * p2`.

### Case 4: The Correct Output Is False Given `x1 = false` and `x2 = false`

Consider `and(bernoulli<bool,1>{false}, bernoulli<bool,1>{false})`.
For this to be true, both must be false positives, which is just
`(1-p1) * (1-p2)`. Since we are interestd in the probability that it maps correctly
to false, that is just `1 - (1-p1) * (1-p2) = p1 + p2 - p1 * p2`.

## Summary

Table 6: `and` with Bernoulli inputs

|`x1` | `x2` | `and(x1,x2)` | `Pr{correct}`       |
|-----|------|--------------|---------------------|
| 1   | 1    | 1            | `p1 * p2`           |
| 1   | 0    | 0            | `1 - p1 + p1 * p2`  |
| 0   | 1    | 0            | `1 - p2 + p1 * p2`  |
| 0   | 0    | 0            | `p1 + p2 - p1 * p2` |

We see that `and : (bernoulli<bool,1>, bernoulli<bool,1>) -> bernoulli<bool,4>`
induces an output that is a fourth-order Bernoulli Boolean. How is this possible
when there are only two possible outputs? The answer is that the output is dependent
on four different combinations of inputs.

Since `x1` and `x2` are *latent*, we can only talk about the probability that
the output is correct or not. We see that when the output is 1, the probability that
the output is correct is `p1 * p2`. When the output is 0, the probability that it is
correct is more complicated.

We could store all of this information in the type `bernoulli<bool,4>`, but it is
probably more convenient to use interval arithmetic, where we store a range of
probabilities for the probabily that the Boolean value being stored is correct.
The best choice is just the minimum length interval that contains all of the
relevant probabilities for the output being correct. When the output is 1, we see
that the minimum spanning interval is just `p1 * p2`, and when the output is 0,
the minimum spanning interval is just the minimum span of
```cpp
min_span{1 - p1 + p1 * p2, 1 - p2 + p1 * p2, p1 + p2 - p1 * p2}
```

As we compose more and more logic circuits together, we can keep track of the
minimum spanning intervals on outputs using interval arithmetic.

Let's come back to the idea of Bernoulli types over compound types. In particular,
let's consider applynig the Bernoulli approximation to binary functions of the
type `(bool, bool) -> bool`.

Now, we can apply the Bernoulli approximation
```cpp
bernoulli<(bool, bool) -> bool>
```
which will generate functions of the type
```cpp
(bool, bool) -> bernoulli<bool>
```

This may be thought of as a *noisy* binary logic-gate.
For the case of the `and` gate, what we observe in our model is
`bernoulli<(bool, bool) -> bool>{and}`, and it can generate up to 16 different
Bernoulli Boolean functions. That means that the maximum order is
$16 (16 - 1) = 240$, which isn't really important, but it's interesting to note.

Of course, if we have this noisy `and` function and then put in noisy inputs,
then we get a function of type
```cpp
(bernoulli<bool>, bernoulli<bool>) -> bernoulli<bool>
```
