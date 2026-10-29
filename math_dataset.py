"""
Math Dataset Module for AI Math Problem Explainer and Error Checker.
Contains 30 rigorously verified mathematics problems across 3 domains:
- 10 Algebra problems
- 10 Probability & Statistics problems
- 10 Calculus Basics problems
Each category spans Easy, Medium, and Hard difficulty levels.
"""

from typing import Dict, List, Any

PROBLEMS: List[Dict[str, Any]] = [
    # =========================================================================
    # ALGEBRA (10 Problems)
    # =========================================================================
    {
        "id": "ALG-01",
        "topic": "Algebra",
        "subtopic": "Linear Equations",
        "difficulty": "Easy",
        "statement": "Solve the linear equation for x: 3x - 7 = 11.",
        "final_answer": "6",
        "acceptable_equivalents": ["6", "x = 6", "x=6", "6.0"],
        "formula": "ax + b = c => ax = c - b => x = (c - b) / a",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Add 7 to both sides of the equation to isolate the variable term.",
                "intermediate_result": "3x = 18",
                "formula_used": "Addition property of equality"
            },
            {
                "step_number": 2,
                "description": "Divide both sides by 3 to solve for x.",
                "intermediate_result": "x = 6",
                "formula_used": "Division property of equality"
            }
        ],
        "common_mistakes": [
            "Subtracting 7 instead of adding 7 (giving 3x = 4 => x = 4/3)",
            "Dividing 11 by 3 before adding 7",
            "Arithmetic error when dividing 18 by 3"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "ALG-02",
        "topic": "Algebra",
        "subtopic": "Factorization",
        "difficulty": "Easy",
        "statement": "Factor the quadratic expression completely: x^2 - 9x + 20.",
        "final_answer": "(x - 4)(x - 5)",
        "acceptable_equivalents": [
            "(x - 4)(x - 5)",
            "(x - 5)(x - 4)",
            "(x-4)(x-5)",
            "(x-5)(x-4)"
        ],
        "formula": "x^2 - (p + q)x + pq = (x - p)(x - q)",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Find two integers whose product is 20 and whose sum is -9.",
                "intermediate_result": "Numbers are -4 and -5 since (-4)*(-5) = 20 and (-4) + (-5) = -9",
                "formula_used": "Vieta's product and sum relations"
            },
            {
                "step_number": 2,
                "description": "Write the quadratic expression in factored binomial form.",
                "intermediate_result": "(x - 4)(x - 5)",
                "formula_used": "Factored form (x + p)(x + q)"
            }
        ],
        "common_mistakes": [
            "Using positive factors (x + 4)(x + 5)",
            "Incorrect signs like (x + 4)(x - 5)",
            "Leaving the expression unfactored or solving for roots without factoring expression"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "ALG-03",
        "topic": "Algebra",
        "subtopic": "Simultaneous Equations",
        "difficulty": "Medium",
        "statement": "Solve the system of linear equations for x and y:\n1) 2x + 3y = 13\n2) x - y = -1",
        "final_answer": "x = 2, y = 3",
        "acceptable_equivalents": [
            "x = 2, y = 3",
            "x=2, y=3",
            "(2, 3)",
            "(2,3)",
            "x = 2 and y = 3",
            "x=2,y=3"
        ],
        "formula": "Substitution or Elimination method for 2x2 linear systems",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Express x in terms of y from the second equation: x = y - 1.",
                "intermediate_result": "x = y - 1",
                "formula_used": "Isolation of variable"
            },
            {
                "step_number": 2,
                "description": "Substitute x into the first equation: 2(y - 1) + 3y = 13.",
                "intermediate_result": "2y - 2 + 3y = 13 => 5y = 15 => y = 3",
                "formula_used": "Substitution method"
            },
            {
                "step_number": 3,
                "description": "Substitute y = 3 back into x = y - 1 to find x.",
                "intermediate_result": "x = 3 - 1 = 2",
                "formula_used": "Back substitution"
            }
        ],
        "common_mistakes": [
            "Sign error when rearranging x - y = -1 to x = y + 1",
            "Distributing 2(y - 1) as 2y - 1 instead of 2y - 2",
            "Reporting only one variable value"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "ALG-04",
        "topic": "Algebra",
        "subtopic": "Quadratic Equations",
        "difficulty": "Medium",
        "statement": "Find all real solutions to the quadratic equation: 2x^2 - 5x + 2 = 0.",
        "final_answer": "x = 2, x = 1/2",
        "acceptable_equivalents": [
            "x = 2, x = 1/2",
            "x = 2, x = 0.5",
            "2, 1/2",
            "2, 0.5",
            "1/2, 2",
            "0.5, 2",
            "x = 1/2 or x = 2",
            "{2, 0.5}"
        ],
        "formula": "x = (-b +/- sqrt(b^2 - 4ac)) / (2a)",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Identify coefficients: a = 2, b = -5, c = 2, and compute the discriminant.",
                "intermediate_result": "D = (-5)^2 - 4(2)(2) = 25 - 16 = 9",
                "formula_used": "Discriminant D = b^2 - 4ac"
            },
            {
                "step_number": 2,
                "description": "Apply the quadratic formula using sqrt(9) = 3.",
                "intermediate_result": "x = (5 +/- 3) / 4",
                "formula_used": "Quadratic formula"
            },
            {
                "step_number": 3,
                "description": "Compute both solutions.",
                "intermediate_result": "x1 = (5 + 3)/4 = 8/4 = 2; x2 = (5 - 3)/4 = 2/4 = 1/2",
                "formula_used": "Simplification"
            }
        ],
        "common_mistakes": [
            "Sign error in -b yielding -5 instead of +5",
            "Dividing only the square root part by 2a instead of the whole numerator",
            "Computing 2a as 2 instead of 2*(2) = 4"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "ALG-05",
        "topic": "Algebra",
        "subtopic": "Exponents and Powers",
        "difficulty": "Medium",
        "statement": "Simplify the exponential expression to a single integer: (2^3 * 4^2) / 8^2.",
        "final_answer": "2",
        "acceptable_equivalents": ["2", "2^1", "2.0"],
        "formula": "(a^m * a^n) = a^(m+n) and (a^m)^k = a^(m*k)",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Express all terms with base 2: 4 = 2^2 so 4^2 = 2^4; 8 = 2^3 so 8^2 = 2^6.",
                "intermediate_result": "Numerator: 2^3 * 2^4 = 2^7; Denominator: 2^6",
                "formula_used": "Power of a power rule"
            },
            {
                "step_number": 2,
                "description": "Divide powers with the same base by subtracting exponents.",
                "intermediate_result": "2^(7 - 6) = 2^1 = 2",
                "formula_used": "Quotient of powers rule: a^m / a^n = a^(m-n)"
            }
        ],
        "common_mistakes": [
            "Multiplying bases instead of adding exponents (e.g. 2^3 * 4^2 = 8^5)",
            "Miscalculating 8^2 in base 2 as 2^5 instead of 2^6",
            "Arithmetic error in exponent subtraction"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "ALG-06",
        "topic": "Algebra",
        "subtopic": "Logarithms",
        "difficulty": "Medium",
        "statement": "Solve for x in the logarithmic equation: log2(x) + log2(x - 2) = 3.",
        "final_answer": "4",
        "acceptable_equivalents": ["4", "x = 4", "x=4", "4.0"],
        "formula": "log_b(M) + log_b(N) = log_b(M*N); log_b(Y) = k => Y = b^k",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Combine the logarithms using the product property.",
                "intermediate_result": "log2(x(x - 2)) = 3",
                "formula_used": "log_b(u) + log_b(v) = log_b(uv)"
            },
            {
                "step_number": 2,
                "description": "Convert logarithmic equation into exponential form.",
                "intermediate_result": "x(x - 2) = 2^3 => x^2 - 2x = 8 => x^2 - 2x - 8 = 0",
                "formula_used": "Definition of logarithm"
            },
            {
                "step_number": 3,
                "description": "Factor the quadratic equation.",
                "intermediate_result": "(x - 4)(x + 2) = 0 => x = 4 or x = -2",
                "formula_used": "Factoring quadratics"
            },
            {
                "step_number": 4,
                "description": "Check the domain of original logarithms (x > 2). Reject extraneous root x = -2.",
                "intermediate_result": "x = 4 is the only valid solution",
                "formula_used": "Logarithm domain constraint: argument must be strictly positive"
            }
        ],
        "common_mistakes": [
            "Failing to discard extraneous root x = -2",
            "Evaluating 2^3 as 6 instead of 8",
            "Writing log2(x) + log2(x - 2) as log2(2x - 2)"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "ALG-07",
        "topic": "Algebra",
        "subtopic": "Nonlinear Systems",
        "difficulty": "Hard",
        "statement": "Find all pairs of real numbers (x, y) that satisfy the system: x + y = 7 and x^2 + y^2 = 25.",
        "final_answer": "(3, 4) and (4, 3)",
        "acceptable_equivalents": [
            "(3, 4) and (4, 3)",
            "(4, 3) and (3, 4)",
            "(3,4) and (4,3)",
            "{(3, 4), (4, 3)}",
            "x = 3, y = 4 or x = 4, y = 3",
            "(3, 4), (4, 3)"
        ],
        "formula": "(x + y)^2 = x^2 + 2xy + y^2",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Square the first equation: (x + y)^2 = 7^2 = 49.",
                "intermediate_result": "x^2 + 2xy + y^2 = 49",
                "formula_used": "Square of a binomial"
            },
            {
                "step_number": 2,
                "description": "Substitute x^2 + y^2 = 25 to find the product xy.",
                "intermediate_result": "25 + 2xy = 49 => 2xy = 24 => xy = 12",
                "formula_used": "Algebraic substitution"
            },
            {
                "step_number": 3,
                "description": "Form the quadratic equation whose roots are x and y: t^2 - 7t + 12 = 0.",
                "intermediate_result": "(t - 3)(t - 4) = 0 => t = 3, 4",
                "formula_used": "Vieta's root theorem"
            },
            {
                "step_number": 4,
                "description": "Conclude the ordered pairs (x, y).",
                "intermediate_result": "(x, y) = (3, 4) or (4, 3)",
                "formula_used": "Symmetric solutions"
            }
        ],
        "common_mistakes": [
            "Assuming x^2 + y^2 = (x + y)^2",
            "Listing only one solution pair (e.g. only (3,4) and omitting (4,3))",
            "Arithmetic mistake when calculating 49 - 25"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "ALG-08",
        "topic": "Algebra",
        "subtopic": "Algebraic Identities",
        "difficulty": "Easy",
        "statement": "Expand and simplify the algebraic square: (2x + 3y)^2.",
        "final_answer": "4x^2 + 12xy + 9y^2",
        "acceptable_equivalents": [
            "4x^2 + 12xy + 9y^2",
            "4*x^2 + 12*x*y + 9*y^2",
            "4x^2 + 9y^2 + 12xy"
        ],
        "formula": "(a + b)^2 = a^2 + 2ab + b^2",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Identify a = 2x and b = 3y.",
                "intermediate_result": "a^2 = (2x)^2 = 4x^2, b^2 = (3y)^2 = 9y^2",
                "formula_used": "Monomial squaring"
            },
            {
                "step_number": 2,
                "description": "Calculate the cross term 2ab.",
                "intermediate_result": "2*(2x)*(3y) = 12xy",
                "formula_used": "Binomial cross product"
            },
            {
                "step_number": 3,
                "description": "Sum the components: a^2 + 2ab + b^2.",
                "intermediate_result": "4x^2 + 12xy + 9y^2",
                "formula_used": "Binomial expansion"
            }
        ],
        "common_mistakes": [
            "Omitting the middle term: writing 4x^2 + 9y^2 (Freshman's dream)",
            "Squaring 2x as 2x^2 instead of 4x^2",
            "Multiplying cross term incorrectly (e.g., 6xy instead of 12xy)"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "ALG-09",
        "topic": "Algebra",
        "subtopic": "Rational Equations",
        "difficulty": "Hard",
        "statement": "Solve the rational equation for x: 2/(x - 1) + 3/(x + 2) = 5x / (x^2 + x - 2).",
        "final_answer": "No solution",
        "acceptable_equivalents": [
            "No solution",
            "no solution",
            "None",
            "phi",
            "empty set",
            "No real solution",
            "contradiction (1 = 0)"
        ],
        "formula": "Multiply by LCD = (x - 1)(x + 2) provided x != 1, x != -2",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Factor the denominator of the right hand side: x^2 + x - 2 = (x - 1)(x + 2). Note domain restrictions: x != 1 and x != -2.",
                "intermediate_result": "LCD = (x - 1)(x + 2)",
                "formula_used": "Factoring quadratics & domain restrictions"
            },
            {
                "step_number": 2,
                "description": "Multiply both sides by (x - 1)(x + 2).",
                "intermediate_result": "2(x + 2) + 3(x - 1) = 5x",
                "formula_used": "Clearing denominators"
            },
            {
                "step_number": 3,
                "description": "Expand and combine like terms.",
                "intermediate_result": "2x + 4 + 3x - 3 = 5x => 5x + 1 = 5x",
                "formula_used": "Distributive property"
            },
            {
                "step_number": 4,
                "description": "Subtract 5x from both sides yielding 1 = 0, an algebraic impossibility.",
                "intermediate_result": "1 = 0 (Contradiction => No solution exists)",
                "formula_used": "Inconsistent equation"
            }
        ],
        "common_mistakes": [
            "Claiming x = 0 is a solution",
            "Claiming all real numbers are solutions",
            "Failing to observe that 5x cancels completely leaving 1 = 0"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "ALG-10",
        "topic": "Algebra",
        "subtopic": "Geometric Series",
        "difficulty": "Hard",
        "statement": "Calculate the exact sum of the infinite geometric series: 6 + 2 + 2/3 + 2/9 + ...",
        "final_answer": "9",
        "acceptable_equivalents": ["9", "9.0", "S = 9", "S=9"],
        "formula": "S = a / (1 - r) for |r| < 1",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Identify the first term a and compute the common ratio r.",
                "intermediate_result": "a = 6; r = 2/6 = 1/3",
                "formula_used": "Common ratio r = T2 / T1"
            },
            {
                "step_number": 2,
                "description": "Verify convergence condition: |r| = 1/3 < 1.",
                "intermediate_result": "Series converges",
                "formula_used": "Convergence criterion |r| < 1"
            },
            {
                "step_number": 3,
                "description": "Apply the infinite sum formula S = a / (1 - r).",
                "intermediate_result": "S = 6 / (1 - 1/3) = 6 / (2/3) = 6 * (3/2) = 18/2 = 9",
                "formula_used": "Infinite geometric series sum formula"
            }
        ],
        "common_mistakes": [
            "Inverting 1 - r as 1/3 instead of 2/3",
            "Multiplying 6 by 2/3 instead of dividing",
            "Using finite sum formula without taking limit"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },

    # =========================================================================
    # PROBABILITY & STATISTICS (10 Problems)
    # =========================================================================
    {
        "id": "PROB-01",
        "topic": "Probability and Statistics",
        "subtopic": "Single-Event Probability",
        "difficulty": "Easy",
        "statement": "A standard fair 6-sided die is rolled once. What is the probability of rolling a prime number?",
        "final_answer": "1/2",
        "acceptable_equivalents": ["1/2", "0.5", "50%", "3/6"],
        "formula": "P(E) = n(E) / n(S)",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "List the sample space of a standard 6-sided die.",
                "intermediate_result": "S = {1, 2, 3, 4, 5, 6}, so n(S) = 6",
                "formula_used": "Sample space definition"
            },
            {
                "step_number": 2,
                "description": "Identify prime numbers in the sample space (numbers > 1 divisible only by 1 and itself).",
                "intermediate_result": "Primes = {2, 3, 5}, so n(E) = 3",
                "formula_used": "Definition of prime numbers"
            },
            {
                "step_number": 3,
                "description": "Compute the probability ratio.",
                "intermediate_result": "P(E) = 3/6 = 1/2 = 0.5",
                "formula_used": "Classical probability formula"
            }
        ],
        "common_mistakes": [
            "Counting 1 as a prime number (yielding 4/6 = 2/3)",
            "Omitting 2 as an even prime",
            "Inverting the ratio as 6/3 = 2"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "PROB-02",
        "topic": "Probability and Statistics",
        "subtopic": "Descriptive Statistics",
        "difficulty": "Easy",
        "statement": "Find the arithmetic mean of the dataset: 4, 7, 7, 8, 9, 10, 11.",
        "final_answer": "8",
        "acceptable_equivalents": ["8", "8.0", "mean = 8", "mean=8"],
        "formula": "x_bar = (sum(x_i)) / n",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Count the number of observations n.",
                "intermediate_result": "n = 7",
                "formula_used": "Sample size count"
            },
            {
                "step_number": 2,
                "description": "Calculate the sum of all observations.",
                "intermediate_result": "4 + 7 + 7 + 8 + 9 + 10 + 11 = 56",
                "formula_used": "Summation"
            },
            {
                "step_number": 3,
                "description": "Divide the sum by n.",
                "intermediate_result": "56 / 7 = 8",
                "formula_used": "Mean formula"
            }
        ],
        "common_mistakes": [
            "Summation error when adding integers",
            "Dividing by 6 instead of 7",
            "Reporting the median or mode instead of the mean"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "PROB-03",
        "topic": "Probability and Statistics",
        "subtopic": "Independent Events",
        "difficulty": "Medium",
        "statement": "Two standard fair six-sided dice are rolled simultaneously. What is the probability that the sum of the numbers shown is equal to 7?",
        "final_answer": "1/6",
        "acceptable_equivalents": ["1/6", "0.1667", "0.167", "6/36", "16.67%"],
        "formula": "P(Sum = 7) = n(outcomes with sum 7) / total outcomes",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Calculate total possible outcomes for two fair 6-sided dice.",
                "intermediate_result": "6 * 6 = 36",
                "formula_used": "Multiplication rule of counting"
            },
            {
                "step_number": 2,
                "description": "Enumerate pairs (d1, d2) that sum to 7.",
                "intermediate_result": "Favorable pairs: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) => 6 outcomes",
                "formula_used": "Systematic enumeration"
            },
            {
                "step_number": 3,
                "description": "Compute the probability ratio and simplify.",
                "intermediate_result": "6 / 36 = 1/6",
                "formula_used": "Classical probability"
            }
        ],
        "common_mistakes": [
            "Counting (1,6) and (6,1) as identical unordered pairs (yielding 3/36 = 1/12)",
            "Using 12 as total outcomes instead of 36",
            "Missing one pair during enumeration"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "PROB-04",
        "topic": "Probability and Statistics",
        "subtopic": "Conditional Probability",
        "difficulty": "Medium",
        "statement": "In a group of 30 students, 18 play soccer, 12 play basketball, and 6 play both sports. If a student chosen at random plays soccer, what is the probability that they also play basketball?",
        "final_answer": "1/3",
        "acceptable_equivalents": ["1/3", "0.3333", "0.333", "6/18", "33.33%"],
        "formula": "P(B | S) = P(B and S) / P(S) = n(B and S) / n(S)",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Identify the given conditioned event: the student plays soccer, so n(S) = 18.",
                "intermediate_result": "Restricted sample space size = 18",
                "formula_used": "Conditioning set definition"
            },
            {
                "step_number": 2,
                "description": "Identify students who play both soccer and basketball: n(B and S) = 6.",
                "intermediate_result": "Intersection size = 6",
                "formula_used": "Intersection of events"
            },
            {
                "step_number": 3,
                "description": "Compute conditional probability P(B | S) = 6 / 18.",
                "intermediate_result": "6 / 18 = 1/3",
                "formula_used": "P(B | S) = n(B and S) / n(S)"
            }
        ],
        "common_mistakes": [
            "Dividing by total students 30 (giving 6/30 = 1/5)",
            "Dividing by basketball players 12 (giving 6/12 = 1/2)",
            "Subtracting 6 from soccer players before dividing"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "PROB-05",
        "topic": "Probability and Statistics",
        "subtopic": "Combinations",
        "difficulty": "Medium",
        "statement": "In how many distinct ways can a committee of 3 people be chosen from a group of 8 candidates?",
        "final_answer": "56",
        "acceptable_equivalents": ["56", "56.0", "C(8,3) = 56", "8C3 = 56"],
        "formula": "C(n, k) = n! / (k! * (n - k)!)",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Set up combination formula with n = 8 and k = 3.",
                "intermediate_result": "C(8, 3) = 8! / (3! * 5!)",
                "formula_used": "Combinations formula"
            },
            {
                "step_number": 2,
                "description": "Cancel out 5! from numerator and denominator.",
                "intermediate_result": "(8 * 7 * 6) / (3 * 2 * 1)",
                "formula_used": "Factorial cancellation"
            },
            {
                "step_number": 3,
                "description": "Simplify the fraction (3 * 2 * 1 = 6 cancels with 6).",
                "intermediate_result": "8 * 7 = 56",
                "formula_used": "Arithmetic simplification"
            }
        ],
        "common_mistakes": [
            "Using permutation formula P(8, 3) = 336 instead of combinations",
            "Arithmetic error multiplying 8 * 7",
            "Forgetting to divide by 3!"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "PROB-06",
        "topic": "Probability and Statistics",
        "subtopic": "Expected Value",
        "difficulty": "Hard",
        "statement": "A game involves rolling a fair six-sided die once. If a 6 is rolled, the player wins $12. If an odd number (1, 3, or 5) is rolled, the player wins $2. If a 2 or 4 is rolled, the player loses $6 (-$6). Find the expected value E(X) of the game in dollars.",
        "final_answer": "1",
        "acceptable_equivalents": ["1", "$1", "1.0", "$1.00", "E(X) = 1"],
        "formula": "E(X) = sum(x_i * P(X = x_i))",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Determine outcomes, monetary payoffs, and their respective probabilities.",
                "intermediate_result": "P(6) = 1/6, payoff = +12; P(odd) = 3/6 = 1/2, payoff = +2; P(2 or 4) = 2/6 = 1/3, payoff = -6",
                "formula_used": "Discrete probability distribution table"
            },
            {
                "step_number": 2,
                "description": "Multiply each payoff by its probability.",
                "intermediate_result": "(12 * 1/6) = 2; (2 * 3/6) = 1; (-6 * 2/6) = -2",
                "formula_used": "x_i * P(x_i)"
            },
            {
                "step_number": 3,
                "description": "Sum the weighted values.",
                "intermediate_result": "2 + 1 + (-2) = 1",
                "formula_used": "Expectation definition"
            }
        ],
        "common_mistakes": [
            "Treating the loss as positive (+6 instead of -6)",
            "Using incorrect probability for odd numbers (e.g. 1/6 instead of 3/6)",
            "Summation error when combining positive and negative gains"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "PROB-07",
        "topic": "Probability and Statistics",
        "subtopic": "Variance",
        "difficulty": "Hard",
        "statement": "Calculate the population variance (sigma^2) of the following population dataset: 2, 4, 4, 4, 5, 5, 7, 9.",
        "final_answer": "4",
        "acceptable_equivalents": ["4", "4.0", "sigma^2 = 4", "sigma^2=4"],
        "formula": "sigma^2 = sum((x_i - mu)^2) / N",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Compute the population mean mu for N = 8.",
                "intermediate_result": "mu = (2 + 4 + 4 + 4 + 5 + 5 + 7 + 9) / 8 = 40 / 8 = 5",
                "formula_used": "Population mean formula"
            },
            {
                "step_number": 2,
                "description": "Compute deviations (x_i - mu) and their squares (x_i - mu)^2.",
                "intermediate_result": "Squares: (2-5)^2=9, (4-5)^2=1, 1, 1, (5-5)^2=0, 0, (7-5)^2=4, (9-5)^2=16",
                "formula_used": "Squared deviations from mean"
            },
            {
                "step_number": 3,
                "description": "Sum the squared deviations.",
                "intermediate_result": "Sum of squared deviations = 9 + 1 + 1 + 1 + 0 + 0 + 4 + 16 = 32",
                "formula_used": "Sum of squares"
            },
            {
                "step_number": 4,
                "description": "Divide by population size N = 8.",
                "intermediate_result": "sigma^2 = 32 / 8 = 4",
                "formula_used": "Population variance definition"
            }
        ],
        "common_mistakes": [
            "Using sample variance divisor (N - 1 = 7) giving 32/7 approx 4.57",
            "Taking the square root (reporting standard deviation 2 instead of variance 4)",
            "Arithmetic error in summing squared deviations"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "PROB-08",
        "topic": "Probability and Statistics",
        "subtopic": "Complementary Probability",
        "difficulty": "Easy",
        "statement": "The meteorological probability of rain tomorrow in a certain city is 0.35. What is the probability that it will NOT rain tomorrow?",
        "final_answer": "0.65",
        "acceptable_equivalents": ["0.65", "65%", "13/20", "0.650"],
        "formula": "P(A') = 1 - P(A)",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "State the rule of complementary events.",
                "intermediate_result": "P(Not Rain) = 1 - P(Rain)",
                "formula_used": "Complement rule"
            },
            {
                "step_number": 2,
                "description": "Substitute P(Rain) = 0.35 and subtract from 1.",
                "intermediate_result": "1 - 0.35 = 0.65",
                "formula_used": "Decimal subtraction"
            }
        ],
        "common_mistakes": [
            "Subtracting incorrectly: 1 - 0.35 = 0.75",
            "Reciprocal mistake: 1 / 0.35",
            "Reporting probability greater than 1"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "PROB-09",
        "topic": "Probability and Statistics",
        "subtopic": "Bayes' Theorem",
        "difficulty": "Hard",
        "statement": "A rare disease affects 1% of a population (P(D) = 0.01). A diagnostic test has a true positive rate (sensitivity) of 95% (P(+|D) = 0.95) and a false positive rate of 5% (P(+|D') = 0.05). If an individual randomly selected from the population tests positive, find the exact posterior probability P(D|+) as a simplified fraction.",
        "final_answer": "19/118",
        "acceptable_equivalents": [
            "19/118",
            "0.1610",
            "0.161",
            "16.1%",
            "0.161017"
        ],
        "formula": "P(D|+) = (P(+|D) * P(D)) / (P(+|D)*P(D) + P(+|D')*P(D'))",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Calculate numerator: P(+ and D) = P(+|D) * P(D) = 0.95 * 0.01.",
                "intermediate_result": "Numerator = 0.0095",
                "formula_used": "Joint probability"
            },
            {
                "step_number": 2,
                "description": "Calculate denominator: total probability of positive test P(+) = P(+|D)*P(D) + P(+|D')*P(D'). Here P(D') = 1 - 0.01 = 0.99.",
                "intermediate_result": "0.0095 + (0.05 * 0.99) = 0.0095 + 0.0495 = 0.0590",
                "formula_used": "Law of total probability"
            },
            {
                "step_number": 3,
                "description": "Compute quotient: 0.0095 / 0.0590 = 95 / 590.",
                "intermediate_result": "Divide numerator and denominator by 5: 95/5 = 19, 590/5 = 118 => 19/118",
                "formula_used": "Fraction simplification"
            }
        ],
        "common_mistakes": [
            "Base rate fallacy: assuming P(D|+) is 95%",
            "Ignoring the false positive contribution (P(+|D')*P(D')) in denominator",
            "Using P(D') = 0.90 instead of 0.99"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "PROB-10",
        "topic": "Probability and Statistics",
        "subtopic": "Binomial Distribution",
        "difficulty": "Medium",
        "statement": "A fair coin is flipped 4 times independently. What is the probability of obtaining exactly 3 heads?",
        "final_answer": "1/4",
        "acceptable_equivalents": ["1/4", "0.25", "25%", "4/16"],
        "formula": "P(X = k) = C(n, k) * p^k * (1 - p)^(n - k)",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Identify binomial parameters: n = 4 trials, k = 3 successes, p = 1/2.",
                "intermediate_result": "n = 4, k = 3, p = 0.5, q = 0.5",
                "formula_used": "Binomial distribution model"
            },
            {
                "step_number": 2,
                "description": "Compute the binomial coefficient C(4, 3).",
                "intermediate_result": "C(4, 3) = 4! / (3! * 1!) = 4",
                "formula_used": "Combinations formula"
            },
            {
                "step_number": 3,
                "description": "Multiply by probability terms: (1/2)^3 * (1/2)^1.",
                "intermediate_result": "4 * (1/8) * (1/2) = 4 * 1/16 = 4/16 = 1/4 = 0.25",
                "formula_used": "Binomial formula"
            }
        ],
        "common_mistakes": [
            "Omitting combination coefficient (calculating (1/2)^4 = 1/16)",
            "Thinking total outcomes is 8 instead of 2^4 = 16",
            "Confusing exactly 3 heads with at least 3 heads"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },

    # =========================================================================
    # CALCULUS BASICS (10 Problems)
    # =========================================================================
    {
        "id": "CALC-01",
        "topic": "Calculus",
        "subtopic": "Power Rule Differentiation",
        "difficulty": "Easy",
        "statement": "Find the derivative of the polynomial function: f(x) = 5x^3 - 4x^2 + 7x - 9.",
        "final_answer": "15x^2 - 8x + 7",
        "acceptable_equivalents": [
            "15x^2 - 8x + 7",
            "15*x^2 - 8*x + 7",
            "f'(x) = 15x^2 - 8x + 7",
            "15x^2-8x+7"
        ],
        "formula": "d/dx(x^n) = n * x^(n - 1)",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Differentiate 5x^3 using power rule: 5 * 3 * x^(3 - 1).",
                "intermediate_result": "15x^2",
                "formula_used": "Constant multiple and power rule"
            },
            {
                "step_number": 2,
                "description": "Differentiate -4x^2 using power rule: -4 * 2 * x^(2 - 1).",
                "intermediate_result": "-8x",
                "formula_used": "Power rule"
            },
            {
                "step_number": 3,
                "description": "Differentiate 7x (gives 7) and constant -9 (gives 0).",
                "intermediate_result": "+7 - 0 = +7",
                "formula_used": "Derivative of linear and constant terms"
            },
            {
                "step_number": 4,
                "description": "Combine the terms.",
                "intermediate_result": "15x^2 - 8x + 7",
                "formula_used": "Sum rule of differentiation"
            }
        ],
        "common_mistakes": [
            "Leaving constant -9 as -9 instead of 0",
            "Decreasing power incorrectly (e.g. 5x^4)",
            "Sign error on the middle term"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "CALC-02",
        "topic": "Calculus",
        "subtopic": "Limits by Factoring",
        "difficulty": "Easy",
        "statement": "Evaluate the limit: lim (x -> 3) [ (x^2 - 9) / (x - 3) ].",
        "final_answer": "6",
        "acceptable_equivalents": ["6", "6.0", "L = 6", "limit = 6"],
        "formula": "a^2 - b^2 = (a - b)(a + b)",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Notice direct substitution x = 3 yields indeterminate form 0/0.",
                "intermediate_result": "(3^2 - 9)/(3 - 3) = 0/0",
                "formula_used": "Direct substitution test"
            },
            {
                "step_number": 2,
                "description": "Factor the numerator as a difference of squares: x^2 - 9 = (x - 3)(x + 3).",
                "intermediate_result": "((x - 3)(x + 3)) / (x - 3)",
                "formula_used": "Difference of squares"
            },
            {
                "step_number": 3,
                "description": "Cancel common factor (x - 3) for x != 3.",
                "intermediate_result": "x + 3",
                "formula_used": "Algebraic cancellation"
            },
            {
                "step_number": 4,
                "description": "Substitute x = 3 into simplified expression.",
                "intermediate_result": "3 + 3 = 6",
                "formula_used": "Continuous function limit substitution"
            }
        ],
        "common_mistakes": [
            "Concluding limit is undefined or 0 because of 0/0",
            "Factoring x^2 - 9 as (x - 3)^2",
            "Arithmetic mistake adding 3 + 3"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "CALC-03",
        "topic": "Calculus",
        "subtopic": "Product Rule",
        "difficulty": "Medium",
        "statement": "Find the first derivative of f(x) = x^2 * e^x.",
        "final_answer": "(x^2 + 2x)*e^x",
        "acceptable_equivalents": [
            "(x^2 + 2x)*e^x",
            "(x^2 + 2x)e^x",
            "x*(x + 2)*e^x",
            "x(x+2)e^x",
            "2x*e^x + x^2*e^x",
            "2xe^x + x^2e^x",
            "e^x*(x^2 + 2x)"
        ],
        "formula": "d/dx[u*v] = u'*v + u*v'",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Set u(x) = x^2 and v(x) = e^x.",
                "intermediate_result": "u'(x) = 2x and v'(x) = e^x",
                "formula_used": "Derivatives of power and exponential functions"
            },
            {
                "step_number": 2,
                "description": "Apply product rule formula: u'v + uv'.",
                "intermediate_result": "(2x)(e^x) + (x^2)(e^x)",
                "formula_used": "Product rule"
            },
            {
                "step_number": 3,
                "description": "Factor out common factor e^x.",
                "intermediate_result": "(x^2 + 2x)e^x or x(x + 2)e^x",
                "formula_used": "Algebraic factoring"
            }
        ],
        "common_mistakes": [
            "Differentiating both terms independently without product rule: 2x * e^x",
            "Dropping one of the terms",
            "Writing derivative of e^x incorrectly"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "CALC-04",
        "topic": "Calculus",
        "subtopic": "Chain Rule",
        "difficulty": "Medium",
        "statement": "Find the derivative of f(x) = sin(3x^2 + 1).",
        "final_answer": "6x*cos(3x^2 + 1)",
        "acceptable_equivalents": [
            "6x*cos(3x^2 + 1)",
            "6x cos(3x^2 + 1)",
            "6*x*cos(3*x^2 + 1)",
            "cos(3x^2 + 1)*6x"
        ],
        "formula": "d/dx[f(g(x))] = f'(g(x)) * g'(x)",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Identify outer function f(u) = sin(u) and inner function u = 3x^2 + 1.",
                "intermediate_result": "f'(u) = cos(u)",
                "formula_used": "Trigonometric derivative rule"
            },
            {
                "step_number": 2,
                "description": "Differentiate inner function with respect to x.",
                "intermediate_result": "u' = d/dx(3x^2 + 1) = 6x",
                "formula_used": "Power rule"
            },
            {
                "step_number": 3,
                "description": "Multiply outer derivative by inner derivative.",
                "intermediate_result": "cos(3x^2 + 1) * 6x = 6x*cos(3x^2 + 1)",
                "formula_used": "Chain rule"
            }
        ],
        "common_mistakes": [
            "Forgetting the inner derivative (answering just cos(3x^2 + 1))",
            "Differentiating sine to -cos instead of +cos",
            "Differentiating 3x^2 as 3x instead of 6x"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "CALC-05",
        "topic": "Calculus",
        "subtopic": "Indefinite Integrals",
        "difficulty": "Easy",
        "statement": "Evaluate the indefinite integral: integral (6x^2 - 4x + 3) dx.",
        "final_answer": "2x^3 - 2x^2 + 3x + C",
        "acceptable_equivalents": [
            "2x^3 - 2x^2 + 3x + C",
            "2*x^3 - 2*x^2 + 3*x + C",
            "2x^3 - 2x^2 + 3x",
            "2*x^3 - 2*x^2 + 3*x"
        ],
        "formula": "integral(x^n dx) = x^(n+1)/(n+1) + C for n != -1",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Integrate term 6x^2: 6 * (x^3 / 3).",
                "intermediate_result": "2x^3",
                "formula_used": "Power rule of integration"
            },
            {
                "step_number": 2,
                "description": "Integrate term -4x: -4 * (x^2 / 2).",
                "intermediate_result": "-2x^2",
                "formula_used": "Power rule of integration"
            },
            {
                "step_number": 3,
                "description": "Integrate constant term 3: 3x.",
                "intermediate_result": "3x",
                "formula_used": "Integration of constant"
            },
            {
                "step_number": 4,
                "description": "Combine terms and append constant of integration C.",
                "intermediate_result": "2x^3 - 2x^2 + 3x + C",
                "formula_used": "Indefinite integral form"
            }
        ],
        "common_mistakes": [
            "Differentiating instead of integrating (giving 12x - 4)",
            "Dividing by n instead of n + 1",
            "Omitting the arbitrary constant + C"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "CALC-06",
        "topic": "Calculus",
        "subtopic": "Definite Integrals",
        "difficulty": "Medium",
        "statement": "Evaluate the definite integral from 0 to 2: integral_{0}^{2} (3x^2 + 2x) dx.",
        "final_answer": "12",
        "acceptable_equivalents": ["12", "12.0", "I = 12", "integral = 12"],
        "formula": "integral_a^b f(x) dx = F(b) - F(a) (Fundamental Theorem of Calculus)",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Find an antiderivative F(x) of 3x^2 + 2x.",
                "intermediate_result": "F(x) = 3*(x^3/3) + 2*(x^2/2) = x^3 + x^2",
                "formula_used": "Antiderivative power rule"
            },
            {
                "step_number": 2,
                "description": "Evaluate F(x) at upper limit x = 2.",
                "intermediate_result": "F(2) = 2^3 + 2^2 = 8 + 4 = 12",
                "formula_used": "Evaluation at upper bound"
            },
            {
                "step_number": 3,
                "description": "Evaluate F(x) at lower limit x = 0.",
                "intermediate_result": "F(0) = 0^3 + 0^2 = 0",
                "formula_used": "Evaluation at lower bound"
            },
            {
                "step_number": 4,
                "description": "Compute F(2) - F(0).",
                "intermediate_result": "12 - 0 = 12",
                "formula_used": "Fundamental Theorem of Calculus Part 2"
            }
        ],
        "common_mistakes": [
            "Arithmetic error: calculating 2^3 as 6 instead of 8",
            "Leaving the expression in terms of x without evaluating bounds",
            "Sign error in F(b) - F(a)"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "CALC-07",
        "topic": "Calculus",
        "subtopic": "U-Substitution Integration",
        "difficulty": "Hard",
        "statement": "Evaluate the indefinite integral: integral 2x * (x^2 + 5)^3 dx.",
        "final_answer": "(x^2 + 5)^4 / 4 + C",
        "acceptable_equivalents": [
            "(x^2 + 5)^4 / 4 + C",
            "((x^2 + 5)^4)/4 + C",
            "1/4*(x^2 + 5)^4 + C",
            "0.25*(x^2 + 5)^4 + C",
            "(x^2 + 5)^4 / 4",
            "1/4*(x^2 + 5)^4"
        ],
        "formula": "integral f(g(x))*g'(x) dx = integral f(u) du",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Substitute u = x^2 + 5.",
                "intermediate_result": "du = 2x dx",
                "formula_used": "Differential substitution"
            },
            {
                "step_number": 2,
                "description": "Rewrite integral completely in terms of u.",
                "intermediate_result": "integral u^3 du",
                "formula_used": "Variable substitution"
            },
            {
                "step_number": 3,
                "description": "Integrate u^3 with respect to u.",
                "intermediate_result": "u^4 / 4 + C",
                "formula_used": "Power rule of integration"
            },
            {
                "step_number": 4,
                "description": "Substitute back u = x^2 + 5.",
                "intermediate_result": "(x^2 + 5)^4 / 4 + C",
                "formula_used": "Back substitution"
            }
        ],
        "common_mistakes": [
            "Forgetting to integrate u^3 (leaving power as 3)",
            "Expanding (x^2 + 5)^3 and making complex expansion mistakes",
            "Dividing by 3 instead of 4"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "CALC-08",
        "topic": "Calculus",
        "subtopic": "Critical Points and Extrema",
        "difficulty": "Hard",
        "statement": "Find the positive critical point x > 0 of the function: f(x) = x^3 - 12x + 5.",
        "final_answer": "2",
        "acceptable_equivalents": ["2", "x = 2", "x=2", "2.0"],
        "formula": "f'(x) = 0 for critical points",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Find the derivative f'(x) using the power rule.",
                "intermediate_result": "f'(x) = 3x^2 - 12",
                "formula_used": "Derivative of polynomial"
            },
            {
                "step_number": 2,
                "description": "Set f'(x) = 0 to find critical numbers.",
                "intermediate_result": "3x^2 - 12 = 0 => 3(x^2 - 4) = 0",
                "formula_used": "Stationary point condition"
            },
            {
                "step_number": 3,
                "description": "Solve for x.",
                "intermediate_result": "x^2 = 4 => x = 2 or x = -2",
                "formula_used": "Square root property"
            },
            {
                "step_number": 4,
                "description": "Select the positive critical point as required by the problem condition (x > 0).",
                "intermediate_result": "x = 2",
                "formula_used": "Domain constraint evaluation"
            }
        ],
        "common_mistakes": [
            "Reporting both x = 2 and x = -2 ignoring condition x > 0",
            "Evaluating f(2) instead of the critical point coordinate x",
            "Solving 3x^2 = 12 incorrectly as x = 4"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "CALC-09",
        "topic": "Calculus",
        "subtopic": "Quotient Rule",
        "difficulty": "Medium",
        "statement": "Find the derivative of the rational function: f(x) = x / (x + 1).",
        "final_answer": "1/(x + 1)^2",
        "acceptable_equivalents": [
            "1/(x + 1)^2",
            "1/(x+1)^2",
            "(x + 1)^(-2)",
            "1 / (x^2 + 2x + 1)"
        ],
        "formula": "d/dx[u/v] = (u'v - uv') / v^2",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Identify u = x and v = x + 1, so u' = 1 and v' = 1.",
                "intermediate_result": "u' = 1, v' = 1",
                "formula_used": "Derivatives of linear terms"
            },
            {
                "step_number": 2,
                "description": "Apply quotient rule: (u'v - uv') / v^2.",
                "intermediate_result": "(1*(x + 1) - x*1) / (x + 1)^2",
                "formula_used": "Quotient rule"
            },
            {
                "step_number": 3,
                "description": "Simplify the numerator: (x + 1 - x) = 1.",
                "intermediate_result": "1 / (x + 1)^2",
                "formula_used": "Algebraic simplification"
            }
        ],
        "common_mistakes": [
            "Reversing the terms in numerator (uv' - u'v giving -1/(x+1)^2)",
            "Differentiating numerator and denominator separately: 1/1 = 1",
            "Forgetting to square the denominator"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    },
    {
        "id": "CALC-10",
        "topic": "Calculus",
        "subtopic": "L'Hopital's Rule / Limits",
        "difficulty": "Hard",
        "statement": "Evaluate the limit: lim (x -> 0) [ (e^(2x) - 1) / x ].",
        "final_answer": "2",
        "acceptable_equivalents": ["2", "2.0", "L = 2", "limit = 2"],
        "formula": "lim [f(x)/g(x)] = lim [f'(x)/g'(x)] for 0/0 (L'Hopital's Rule)",
        "reference_steps": [
            {
                "step_number": 1,
                "description": "Check indeterminate form: as x -> 0, e^0 - 1 = 0 and denominator = 0 (form 0/0).",
                "intermediate_result": "Indeterminate form 0/0 verified",
                "formula_used": "Direct substitution check"
            },
            {
                "step_number": 2,
                "description": "Apply L'Hopital's Rule: differentiate numerator and denominator with respect to x.",
                "intermediate_result": "d/dx(e^(2x) - 1) = 2*e^(2x) and d/dx(x) = 1",
                "formula_used": "L'Hopital's Rule & chain rule"
            },
            {
                "step_number": 3,
                "description": "Evaluate limit of quotient of derivatives as x -> 0.",
                "intermediate_result": "lim (x -> 0) [ 2*e^(2x) / 1 ] = 2*e^0 / 1 = 2*1 = 2",
                "formula_used": "Limit evaluation"
            }
        ],
        "common_mistakes": [
            "Differentiating e^(2x) as e^(2x) forgetting factor of 2 (giving 1)",
            "Using quotient rule instead of differentiating top and bottom separately",
            "Claiming limit is 0 or undefined"
        ],
        "verification_status": "Independently Verified by SymPy & Reference"
    }
]

def get_all_problems() -> List[Dict[str, Any]]:
    """Return all 30 problems."""
    return PROBLEMS

def get_problem_by_id(problem_id: str) -> Dict[str, Any]:
    """Retrieve problem by unique ID."""
    for p in PROBLEMS:
        if p["id"].upper() == problem_id.upper():
            return p
    return None

def get_problems_by_topic(topic: str) -> List[Dict[str, Any]]:
    """Filter problems by topic."""
    return [p for p in PROBLEMS if p["topic"].lower() == topic.lower()]

def get_problems_by_difficulty(diff: str) -> List[Dict[str, Any]]:
    """Filter problems by difficulty."""
    return [p for p in PROBLEMS if p["difficulty"].lower() == diff.lower()]
