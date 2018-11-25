#ifndef NEWGAMEOFLIFEXL_GAMEOFLIFE_H
#define NEWGAMEOFLIFEXL_GAMEOFLIFE_H

#include <cstddef>
#include <vector>
#include <algorithm>
#include <iostream>

#include "Rule.hpp"

namespace GoL {

    template <typename T>
    using table_t = std::vector<std::vector<T>>;

    template<typename T = bool>
    class GoLEngine {
    public:
        GoLEngine() : m_rule(CONWAY), max_x(1), max_y(1) { }
        GoLEngine(std::size_t max_x, std::size_t max_y, const Rule<T> & rule = CONWAY) :
                m_rule{rule} , max_x{max_x}, max_y{max_y} , m_table(max_x, std::vector<T>(max_y, T() )) { }

        void setRule(const Rule<T> & rule) { m_rule = rule; }
        virtual void run(size_t iter);
        void run() { run(1); }
        Rule<T> getRule() const { return m_rule; }
        T get(int x, int y) const { return m_table.at((x+max_x)%max_x).at((y+max_y)%max_y); }
        void set(size_t x, size_t y, T state) { m_table.at(x).at(y) = state; }
        void reset();
        unsigned long long int getGen() const { return m_gen; }
        size_t getXMax() const { return max_x; }
        size_t getYMax() const { return max_y; }
    protected:
        // Useful Function
        virtual void run_once(table_t<T> & tmp_table);
        size_t counting_full(int x, int y) const;
        inline bool is_confine(size_t x, size_t y) const {
            return ( x == 0 || x == max_x -1 || y == 0 || y == max_y -1);
        }
        // Attributes
        Rule<T> m_rule;
        unsigned long long int m_gen = 0; // Generazione
        size_t max_x, max_y;
        table_t<T> m_table;
    };

    template<typename T>
    void GoLEngine<T>::reset() {
        for (auto & ax : m_table)
            std::fill(ax.begin(), ax.end(), T() );
        m_gen = 0;
    }

    template<typename T>
    size_t GoLEngine<T>::counting_full(int x, int y) const {
        size_t full = 0;
        for(auto i = x-1; i <= x+1; i++)
            for(auto j = y-1; j <= y+1; j++) {
                if(i == x and j == y) continue;
                if(this->get(i,j)) full++;
            }
        return full;
    }

    template<typename T>
    void GoLEngine<T>::run(size_t iter) {
        table_t<T> tmp_table = m_table;
        for(size_t i = 0; i < iter; i++) {
            run_once(tmp_table);
            m_table = tmp_table;
            m_gen++;
        }
    }

    template<typename T>
    void GoLEngine<T>::run_once(table_t<T> & tmp_table) {
        for(size_t i = 0; i < max_x; i++)
            for(size_t j = 0; j < max_y; j++) {
                size_t full = counting_full(i, j);
                tmp_table.at(i).at(j) = m_rule.apply(full, m_table.at(i).at(j));
            }
    }
}

#endif //NEWGAMEOFLIFEXL_GAMEOFLIFE_H
