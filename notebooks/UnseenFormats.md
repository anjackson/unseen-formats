---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.2
kernelspec:
  name: python3
  display_name: Python 3 (ipykernel)
  language: python
---

# Unseen Formats

Format Diversity Estimation

Estimating the total number of digital formats

This analysis uses data from the various registries to build a [Species Accumulation Curve](https://en.wikipedia.org/wiki/Species_discovery_curve), which is an approach used in ecology to estimate the number of species in a given ecosystem[^1]. If we treat each format registry as a random sample of the whole ecosystem of data formats, we can combine the series of samples and count how many new formats are added each time a sample is added to the overall set. Overall, the number of new formats being discovered would be expected to decrease as more samples are added, roughly converging towards an estimate for the total global diversity of digital data formats.

[^1]: Ugland, K.I., Gray, J.S. and Ellingsen, K.E. (2003), The species–accumulation curve and estimation of species richness. Journal of Animal Ecology, 72: 888-897. <https://doi.org/10.1046/j.1365-2656.2003.00748.x>


## Method

We start by looking at the overall 'uniqueness' of each registry, by looking at how many extensions are unique to each registry.

We then sort the registries in order of descending overall sample size (e.g. how many distinct extensions each holds), and treat each one as a sample of the total set of data formats.  We add each in turn, counting the new extensions at each step, with each sample.

Finally, we fit a curve to this data based on the expected form, and extrapolate to determine an estimate for the total number of data formats.

Because we are reducing all the registry data down to file extensions, the assumptions and caveats outlined [here](https://www.digipres.org/workbench/formats/#file-extensions) should be kept in mind.  In particular, given that multiple distinct formats may use the same file extension, this analysis should be considered as establishing a conservative lower-bound on the number of formats.

## Uniqueness

To understand how distinct the holdings of each registry are, we can plot the percentage of unique entries versus the total number of entries.  If all registries were truly random samples of the totality of data formats, we would expect a broadly linear trend. In other words, we would expect larger registries to contain a larger percentage of unique entries.

```{code-cell} ipython3
from unseen_formats.species import load_extensions, compute_sac
import pandas as pd

ext_sets = load_extensions('../data/extensions-new-2025-08-12.json')
results = compute_sac(ext_sets)

df = pd.DataFrame(results)
num_points = len(df['source'])

df
```

```{code-cell} ipython3
%matplotlib inline
import matplotlib_inline
matplotlib_inline.backend_inline.set_matplotlib_formats('svg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
plt.rcParams['font.size'] = '14'
figsize = (9, 6)

fig, ax = plt.subplots(figsize=figsize)
for i in range(num_points):
    b = ax.bar(df['source'][i],df['num_exts'][i])
    ax.bar_label(b, fontsize=11)

ax.tick_params("x", rotation=45)
plt.ylabel('Number of File Extensions')

plt.savefig('unseen-registries.svg')
plt.show()
```

```{code-cell} ipython3
fig, ax = plt.subplots(figsize=figsize)
for i in range(num_points):
    x = df['num_exts'][i]
    max_x = max(df['num_exts'])
    y = df['percent_uniq_exts'][i]
    max_y = max(df['percent_uniq_exts'])
    txt = df['source'][i]
    ax.scatter(x, y, label=txt, s=30, zorder=10)
    if txt != 'lcfdd':
        lr = 'left'
        offset = (4,0)
    else:
        lr = 'right'
        offset = (-4,0)
    ax.annotate(txt, (x, y), xytext=offset, textcoords='offset points', 
                ha=lr, fontsize=11, zorder=5,
                path_effects=[pe.withStroke(linewidth=4, foreground="white")])
    
ax.set_xlim([0, 9000])
ax.set_ylim([0, 50])

#plt.legend(fontsize=9)
plt.grid(True, linestyle='--', alpha=0.6, zorder=2)
plt.xlabel('Number of File Extensions')
plt.ylabel('Unique File Extensions')
plt.savefig('unseen-uniqueness.svg')
plt.show()
```

This plot shows that different registries have their own character. For example, as one might expect the GitHub Linguist set has a large number of distinct entries, especially given it's relatively small size. This is likely because it specialises in looking at source code files and related formats likely to be found in GitHub repositories.

It is notable that the `fdd` and `pronom` have relatively low percentages of unique extensions. This makes sense as it reflects the way those efforts have tended to prioritise coverage of the most widely used formats.


## Species Accumulation Curve

The results of the final species accumulation curve are shown below.

```{code-cell} ipython3
from unseen_formats.fit import generate_fit

x_fit, y_fit, a_opt, b_opt, y_lower, y_upper = generate_fit(df['total_exts'], df['total_uniq_exts'], 2000, 50000)


# Plot the original data
fig, ax = plt.subplots(figsize=figsize)
for i in range(len(df['source'])):
    ax.scatter(df['total_exts'][i], df['total_uniq_exts'][i], label=df['source'][i], s=20)

# Plot the fitted curve
#plt.plot(x_fit, y_fit, 'r-', label=None, alpha=0.1)

# Plot the 95% confidence interval
#plt.fill_between(x_fit, y_lower, y_upper, color='red', alpha=0.2, label='95% Confidence Interval')

# Set the limits
ax.set_xlim([0, 50000])
ax.set_ylim([0, 14000])

# Final plot styling
plt.xlabel('Total File Extensions Recorded')
plt.ylabel('Total Unique File Extensions')
plt.legend(fontsize=11, loc='lower right')
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig('unseen-sac.svg')
plt.show()
```

```{code-cell} ipython3
# Plot the original data
fig, ax = plt.subplots(figsize=figsize)
for i in range(len(df['source'])):
    ax.scatter(df['total_exts'][i], df['total_uniq_exts'][i], label=None, s=20)

# Plot the fitted curve
plt.plot(x_fit, y_fit, 'r-', label=f'Fit: y = {a_opt:.2f}ln(x) + {b_opt:.2f}')

# Plot the 95% confidence interval
plt.fill_between(x_fit, y_lower, y_upper, color='red', alpha=0.2, label='95% Confidence Interval')

# Set the limits
ax.set_xlim([0, 50000])
ax.set_ylim([0, 14000])

# Final plot styling
plt.xlabel('Total File Extensions Recorded')
plt.ylabel('Total Unique File Extensions')
plt.legend(fontsize=11, loc='lower right')
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig('unseen-sac-fit.svg')
plt.show()
```

This indicates that a conservative lower-bound on the total number of formats we might expect to come across is around 12,000, but given the variation between the data points and the fitted curve, this is only an approximate answer.

## Conclusions

Even allowing for a significant degree of error in the estimation process, it is clear that the total number of formats we wish to understands is well in excess of even the many thousands of records in _WikiData_.

This has significant consequences for the handling of digital material. These include:

- As the majority of formats are _not_ known to PRONOM, it is _not_ appropriate to block the ingest of _born-digital_ items into the safe storage space of a repository service just because it cannot be identified yet.
- Digital repositories should make it easy to re-run format identification processes across our collections, as the tools improve.

Further work is required to understand:

- The size of collections that remain unknown.
- How the distribution of importance or value is or is not related to format.
- The costs and human effort required to populate registries.
- Whether centralised approaches to registries can cope with these realities.
- What other approaches might work, and what are the consequences.

The work on [Using Collection Profiles](https://www.digipres.org/workbench/formats/profiles) aims to help explore some of these issues.

```{code-cell} ipython3

```
