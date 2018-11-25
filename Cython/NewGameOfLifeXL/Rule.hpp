#ifndef NEWGAMEOFLIFEXL_RULE_H
#define NEWGAMEOFLIFEXL_RULE_H

#include <cstddef>
#include <vector>
#include <algorithm>
#include <stdexcept>

namespace GoL {

    template <typename T = bool>
    class Rule {
    public:
        Rule() = default;
        Rule(const std::vector<size_t> & B, const std::vector<size_t> & S);
        Rule(const Rule & old) = default;
        ~Rule() = default;

        T apply(size_t full, T state) const;
        std::vector<size_t> getBirth() const { return m_Birth; }
        std::vector<size_t> getStay() const { return m_Stay; }
    protected:
        std::vector<size_t> m_Birth;
        std::vector<size_t> m_Stay;
    };

    template <typename T>
    Rule<T>::Rule(const std::vector<size_t> & B, const std::vector<size_t> & S) {
        if (std::any_of(B.begin(), B.end(), [](size_t n){ return (n < 0 || n > 8); }))
            throw std::range_error("Birth Rule must be between 0 and 8.");
        if (std::any_of(S.begin(), S.end(), [](size_t n){ return (n < 0 || n > 8); }))
            throw std::range_error("Birth Rule must be between 0 and 8.");
        m_Birth = B;
        m_Stay = S;
    }

    template <typename T>
    T Rule<T>::apply(size_t full, T state) const {
        if(state) {
            return std::find(m_Stay.begin(), m_Stay.end(), full) != m_Stay.end();
        } else {
            return std::find(m_Birth.begin(), m_Birth.end(), full) != m_Birth.end();
        }
    }

    const Rule<bool> CONWAY({3}, {3,2});
}

#endif //NEWGAMEOFLIFEXL_RULE_H
