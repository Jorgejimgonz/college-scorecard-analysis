# College Scorecard: Higher Education Outcomes
## Written Narrative
### Jorge Jimenez | CS 4379G — Data Analysis & Visualization | Spring 2026

---

## Research Question

Does paying more or attending a more selective school actually lead to 
better outcomes for students? This project uses the U.S. Department of 
Education College Scorecard dataset to compare two inputs — tuition cost 
and institutional selectivity — against two outputs — graduation rates and 
median earnings 10 years after enrollment. The goal is to determine whether 
expensive, selective schools consistently produce better financial results, 
or whether some institution types offer a stronger return on investment.

This question matters because prospective students and their families make 
one of the biggest financial decisions of their lives when choosing a college. 
The assumption that a more expensive or more prestigious school automatically 
leads to better outcomes is deeply embedded in how we think about higher 
education. This project challenges that assumption with real data.

---

## Methodology

The College Scorecard dataset was downloaded from the U.S. Department of 
Education and contains data on 6,322 institutions across 3,308 variables. 
The dataset was trimmed to 11 relevant columns covering cost, selectivity, 
graduation rates, earnings, and institutional characteristics.

The cleaning pipeline filtered the dataset to 4-year degree granting 
institutions only, since comparing community colleges to research universities 
would not be a fair or meaningful comparison. Rows missing any of the four 
key metrics were dropped, resulting in a final clean dataset of 1,474 
institutions. A return on investment column was engineered by dividing median 
earnings by annual cost of attendance, providing a direct measure of financial 
value per dollar spent.

---

## Key Findings

**Finding 1: Cost does not reliably predict earnings.**
A scatter plot of annual cost against median earnings 10 years after 
enrollment reveals no consistent upward trend. While some expensive schools 
do produce high earners, many do not. Some of the lowest cost institutions 
produce graduates who out-earn those from significantly more expensive schools. 
This suggests that tuition price alone is a poor signal of educational quality 
or financial return.

**Finding 2: Cost does not reliably predict graduation rates either.**
When cost is compared against 6-year graduation rates, the same pattern 
emerges. Expensive schools do not consistently graduate more of their students. 
Some open admission public schools achieve graduation rates that rival those 
of costly private institutions, suggesting that factors beyond price drive 
student completion.

**Finding 3: Selectivity has a weak relationship with earnings.**
More selective schools — those with lower admission rates — show a slight 
tendency toward higher graduate earnings. However the relationship is weak 
and inconsistent. There are many highly selective schools whose graduates 
earn average salaries, and many less selective schools whose graduates earn 
well above average. Selectivity alone is not a reliable predictor of 
financial outcomes.

**Finding 4: Graduation rate is the strongest predictor of earnings.**
A correlation analysis of all key metrics revealed that graduation rate has 
the strongest positive relationship with median earnings — stronger than 
either cost or selectivity. Schools that successfully get students across 
the finish line consistently produce better financial outcomes. This suggests 
that institutional support and student success infrastructure matter more 
than price or prestige.

**Finding 5: Public schools deliver the best return on investment.**
Despite being perceived as less prestigious than private institutions, public 
schools dominate the top of the ROI rankings. Their lower cost of attendance 
combined with competitive graduate earnings means that students get more 
financial value per dollar spent. The top ROI school in the entire dataset 
is a public Maritime Academy — not an Ivy League institution.

---

## Limitations

**Missing data:** A significant portion of institutions were dropped due to 
missing values in key metrics. Smaller and newer institutions are less likely 
to report complete data, which means our analysis skews toward larger and 
more established schools. The findings may not fully represent the complete 
landscape of U.S. higher education.

**Earnings data timing:** The median earnings figure captures graduates 10 
years after enrollment, not 10 years after graduation. Students who took 
longer to finish or who dropped out are included in this number, which may 
understate the true earnings of graduates from schools with lower completion 
rates.

**ROI simplification:** Our ROI calculation divides median earnings by annual 
cost of attendance. This does not account for financial aid, scholarships, 
or the number of years a student actually attends. A student who receives a 
full scholarship to a private school would have a very different real ROI 
than what our formula captures.

**Correlation is not causation:** Finding that graduation rate correlates 
with earnings does not mean that graduating from any school causes higher 
earnings. Students who graduate may differ from those who do not in ways 
that independently affect their earnings, such as motivation, family 
background, or field of study.

---

## Conclusion

The data tells a clear and perhaps surprising story. The conventional wisdom 
that spending more or attending a harder to get into school leads to better 
outcomes is not consistently supported by the evidence. What matters most 
is whether students actually finish their degree, and whether the cost of 
that degree is reasonable relative to the earnings it produces. Public 
institutions, often overlooked in favor of prestigious private schools, 
consistently offer the strongest financial return on investment. For 
prospective students making one of the biggest financial decisions of their 
lives, these findings suggest that value, fit, and likelihood of graduation 
may matter far more than price tag or selectivity.