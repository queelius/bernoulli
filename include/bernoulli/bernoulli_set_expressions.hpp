#pragma once

// --- bernoulli_set_expr.hpp ---

namespace bernoulli::set::algebra
{
    template <typename E>
    class bernoulli_set_expr
    {
    public:
    	using value_type = typename E::value_type;

        bernoulli_set_expr(E const & e) : e(e) {}

        auto error_rate(T const & x) { return static_cast<E>(e).error_rate(x); }
        auto false_positive_rate() const { return static_cast<E>(e).false_positive_rate(); }
        auto false_negative_rate() const { return static_cast<E>(e).false_negative_rate(); }
        auto contains( const & x) const { return static_cast<E>(e).contains(x); }

    private:
        E const & e;
    };
}

// --- bernoulli_set_complement_expr.hpp ---

#include "bernoulli_set_expr.hpp"

namespace bernoulli::set::algebra
{
    template <typename S>
    struct bernoulli_set_complement_expr:
        public bernoulli_set_expr<bernoulli_set_complement_expr<S>>
    {
        using value_type = S::value_type;

        bernoulli_set_complement_expr(S const & s) : s_(s) {}

        auto fpr() const { return s.fnr(); }
        auto fnr() const { return s.fpr(); }
        auto contains(value_type const & x) { return !s_.contains(x); }

        S const & s_;
    };

    template <typename S> // S models the concept of a bernoulli set
    auto make_complement(S const & s)
    {
        return bernoulli_set_complement_expr<S>(s);
    }
}

// --- bernoulli_set_union_expr.hpp ---

#include "bernoulli_set_expr.hpp"

namespace bernoulli::set::algebra
{
    template <typename L, typename R>
    struct bernoulli_set_union_expr: public bernoulli_set_expr<bernoulli_set_union_expr<L,R>>
    {
        using value_type = L::value_type;

        bernoulli_set_union_expr(
            L const & left,
            R const & right)
            : left_(left), right_(right) {}

        auto fpr() const
        {
            return interval<double>(1)-(interval<double>(1)-lfpr())*
                   (interval<double>(1)-rfpr());
        }

        auto lfpr() const { return interval<double>(left_.fpr()); }
        auto rfpr() const { return interval<double>(right_.fpr()); }
        auto lfnr() const { return interval<double>(left_.fnr()); }
        auto rfnr() const { return interval<double>(right_.fnr()); }

        auto fnr() const
        {
            return min_span(lfnr() * rfnr(),
                            lfnr() * (interval<double>(1)-rfpr()),
                            lfnr() * (interval<double>(1)-rfpr()));
        }

        auto contains(value_type const & x)
        {
            return left_.contains(x) || right_.contains(x);
        }

        L const & left_;
        R const & right_;
    };

    template <
        typename L, // L models the concept of a bernoulli set
        typename R  // R models the concept of a bernoulli set
    >
    auto make_union(L const & left, R const & right)
    {
        return bernoulli_union_set_expr<L,R>(left,right);
    }
}

// --- bernoulli_set_intersection_expr.hpp ---

#include "bernoulli_set_expr.hpp"

namespace bernoulli::set::algebra
{
    template <typename L, typename R>
    struct bernoulli_set_intersection_expr:
        public bernoulli_set_expr<bernoulli_set_intersection_expr<L,R>>
    {
        using value_type = L::value_type;

        constexpr interval<double> one() { return interval<double>(1) }

        bernoulli_set_intersection_expr(
            L const & left,
            R const & right)
            : left_(left), right_(right) {}

        auto fpr() const
        {
            return one() - (one() - left_.fpr()) * (one() - right_.fpr());
        }

        auto fnr() const
        {
            return span(
                left_.fnr() * right_.fnr(),
                span(left_.fnr()*(one()-right_.fpr()),
                    right_.fnr()*(one()-left_.fpr())));
        }


        auto contains(value_type const & x)
        {
            return left_.contains(x) && right_.contains(x);
        }

        L const & left_;
        R const & right_;
    };

    template <
        typename L, // L models the concept of a bernoulli set
        typename R  // R models the concept of a bernoulli set
    >
    auto make_intersection(L const & left, R const & right)
    {
        return bernoulli_intersection_set_expr<L,R>(left,right);
    }
}

// --- bernoulli_set_disjoint_union_expr.hpp ---

#include "bernoulli_set_expr.hpp"

template <
    typename L,
    typename R
>
class bernoulli_disjoint_union_set_expr:
    public bernoulli_set_expr<bernoulli_disjoint_union_set_expr<L,R>>
{
public:
    using left_value_type = typename L::value_type;
    using right_value_type = typename R::value_type;
    using value_type = std::variant<
        left_value_type,
        right_value_type>;

    bernoulli_disjoint_union_set_expr(
        L const & left,
        R const & right) : left_(left), right_(right) {};

    auto left() const { return left; }
    auto right() const { return right; }

    auto contains(left_value_type const & x) { return left.contains(x); }
    auto contains(right_value_type const & x) { return right.contains(x); }

private:
    L const & left_;
    R const & right_;
};

template <
    typename L,
    typename R
>
auto
make_disjoint_union(L left, R right)
{
    return bernoulli_disjoint_union_set_expr<L,R>(left,right);
}

// --- bernoulli_set_cartesian_expr.hpp ---

#include "bernoulli_set_expr.hpp"

namespace bernoulli::set::algebra
{
    template <
        typename L,
        typename R
    >
    class bernoulli_set_cartesian_prod_expr:
        public bernoulli_set_expr<bernoulli_set_cartesian_prod_expr<L,R>>
    {
    public:
        bernoulli_set_cartesian_prod_expr(L const & left, R const & right)
            : left_(left), right_(right) {};

        using left_value_type = typename L::value_type;
        using right_value_type = typename R::value_type;
        using value_type = std::pair<left_value_type,right_value_type>;

        /**
         * Note that `left.contains` and `right.contains` are typically
         * Bernoulli Booleans, which implement `&&`, i.e.,
         * ```
         *     && : (bernoulli_bool<N1>, bernoulli_bool<N2> -> bernoulli_bool<N3>
         * ```
         * and thus `contains` returns a Bernoulli Boolean that models
         * `bernoulli_bool<N2>`.
         */
        auto contains(value_type const & p) const
        {
            return left_.contains(p.first) && right_.contains(p.second);
        }

        auto fpr() const
        {
            throw "not implemented yet";
        }

        auto tpr() const
        {
            throw "not implemented yet";
        }

        auto left() const { return left_; }
        auto right() const { return right_; }

        auto flip() const { return bernoulli_set_cartesian_prod_expr<R,L>(right_,left_) }

        L const & left_;
        R const & right_;
    };

    template <
        typename L,
        typename R
    >
    auto
    make_cartesian_product(L const & left, R const & right)
    {
        return bernoulli_set_cartesian_prod_expr<L,R>(left,right);
    }
}

// --- bernoulli_set_power_expr.hpp ---

template <typename B>
class bernoulli_power_set_expr: bernoulli_set_expr<bernoulli_power_set_expr<B>>
{
public:
    bernoulli_power_set_expr(B const & bs) : bs(bs) {};

    using value_type = std::set<typename B::value_type>;

    auto contains(value_type const & s) const
    {
        bernoulli_bool<X,2> res(true,0,0)
        for (auto const & x : s)
            res = res && contains(x);
        return res;
    }

    auto fpr() const
    {
        return interval<double>(0,1);
    }

    auto fnr() const
    {
        return interval<double>(0,1);
    }

private:
    B const & bs;
};

// --- bernoulli_set_union_exp.hpp ---

template <bernoulli_set A, bernoulli_set B>
struct bernoulli_set_union_exp:
    public bernoulli_set_exp<bernoulli_set_union_exp<A,B>>
{
    using value_type = typename A::value_type;

    auto contains(value_type const & x) { return a.contains(x)||b.contains(x); };

    auto error(value_type const & x)
    {
        1-implicit_probability(x);
    }

    auto false_positive_rate() const
    {
        using T = decltype(a.false_positive_rate());

        return T(1)-
            (T(1)-a.false_positive_rate())*(T(1)-b.false_positive_rate());
    }

    auto false_negative_rate() const
    {
        using std::min;
        using std::max;
        using T = decltype(a.false_positive_rate())

        auto p1 = a.false_negative_rate() * b.false_negative_rate(),
             p2 = a.false_negative_rate()*(T(1)-b.false_positive_rate()),
             p3 = b.false_negative_rate()*(T(1)-a.false_positive_rate());

        return std::pair<T,T>{min(min(p1,p2),p3),max(max(p1,p2),p3)};
    }

    A const & a;
    B const & b;
};

template <bernoulli_set A, bernoulli_set B>
auto make_union_exp(A a, B b)
{
    return bernuolli_set_union_exp<A,B>{ }
}
