#pragma once
#include <memory>

// --- reflexive_bernoulli_relation.hpp ---

template <typename R>
struct reflexive_bernoulli_relation
{
public:
    using value_type = typename R::value_type;

    reflexive_bernoulli_relation(R r) : r_(r) {}

    // if (x1, ..., xn) in R then all permutations of (x1, ..., xn) are in R.
    bool contains(value_type const & xs) const
    {
        for (auto const & p : permutations(xs.begin(),xs.end()))
        {
            if (r.contains(p))
                return true;
        }
        return false;
    }

    R r;
};

// --- symmetric_bernoulli_relation.hpp ---

namespace bernoulli
{
  // R models a bernoulli symmetric relation.
  template<typename R>
  struct symmetric_bernoulli_relation
  {
    using X = typename R::left_value_type;
    using Y = typename R::right_value_type;

    public:
      // value_type should be some sort of pair type
      // where each element is of the same type,
      // otherwise symmetry should not be possible.
      using value_type = std::pair<X,Y>;

      bool

      // we enforce the invariant that (x, y) in R
      // iff (y, x) in R.
      bool contains(X const & x, Y const & y) const
      {
          return r.contains(x,y) || r.contains(y,x);
      }

      R r;
  };
}
