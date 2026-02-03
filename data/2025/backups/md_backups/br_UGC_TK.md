SPECIAL CRITERIA
----------------

**SC1: Does the platform offer an API for collecting public
user-generated content data?** - weight 0.30

This item verifies whether the platform provides an API with at least
one endpoint for programmatically extracting public user-generated
content to the users' infrastructure. Public user-generated content is
defined here as any publicly visible publication accessible by any
platform user. The assessment should verify that the endpoint allows
retrieval and storage of this content without requiring privileged or
internal access beyond standard developer registration.

-   Yes

-   Yes, but only for approved researchers

-   **No**

**Justification:**

TikTok does offer research tools, but access is limited to researchers
who are based in or affiliated with academic institutions in the United
States, the European Economic Area, the United Kingdom, or Switzerland,
as well as those affiliated with non-profit or independent research
institutions, organizations, associations, or bodies within the European
Union ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).
As Brazil -- and most of the world -- fall outside this scope,
researchers in other regions are limited to data scraping capabilities
([[Chemillier et al.,
2022]{.underline}](https://hal.science/hal-04454074/)).

**SC2: Can the full scope of public content data be extracted through
the platform's API?** - weight 0.30

This item verifies whether the platform enables programmatic discovery
and extraction of data from the complete set of public user-generated
content. The assessment should confirm that the API provides access to
all types of public content on the platform, without exclusions or
artificial restrictions that limit data completeness.

-   Yes

-   Yes, but only for approved researchers

-   **No**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

**SC3: Is access to the platform's API free of charge?** - weight 0.30

This item verifies whether API use is free of charge, since even modest
fees can create barriers or force researchers in low-resourced settings
to narrow the scope of their work. The assessment should verify the
platform's documentation and pricing policies to confirm that no fees
are applied for API access.

-   Yes

-   Yes, but only for approved researchers

-   **No**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

**SC4: Does the platform offer a graphical interface for extracting
data?** - weight 0.10

This item verifies whether the platform offers a graphical interface for
observing and collecting data to the users' infrastructure. The data
should be equivalent to that which is available through the API or the
default user interface. The assessment should confirm the existence of
an official tool, such as a dashboard or export feature, that allows
extracting public content data without programming.

-   Yes

-   Yes, but only for approved researchers

-   **No**

**Justification:**

In the same way that it does not provide an API enabling programmatic
access to or extraction of public user-generated content data for
researchers based in Brazil or affiliated with Brazilian institutions,
TikTok likewise does not offer a graphical interface for this purpose.

OTHER CRITERIA
--------------

### ACCESSIBILITY

*Accessibility measures how easily data can be located, retrieved,
understood and used.*

**OC1: Does the platform offer any type of access to non-public data
(e.g., private groups, not direct messages) to approved researchers?**

This item verifies whether, beyond the retrieval and extraction of
public user-generated content data, the API permits the extraction of
any data from non-public content, such as posts and comments in private
groups or discussion forums, subject to the implementation of adequate
data hashing measures and specific researcher approval. The assessment
should confirm that the API provides such access measures, either
through specific endpoints or other controlled access mechanisms.

-   Yes

-   **No**

**Justification:**

TikTok does not provide any form of access to or extraction of
non-public user-generated content data for researchers based in Brazil
or affiliated with Brazilian institutions.

**OC2: Can the requested data be extracted directly from the platform's
API response?**

This item verifies whether the API returns structured data directly in
its response, rather than only providing a redirect link to the data.
Audiovisual media (e.g., images, videos, and audio) are excluded from
this assessment. The assessment should check sample API responses to
confirm that the requested public data is included in the returned
payload itself.

-   Yes

-   **No**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

**OC3: Does the platform's API provide a form of authentication that
allows for token renewal without the risk of data loss?**

This item verifies whether the tokens provided for API use can be
renewed without risk of data loss, ensuring continuity and integrity of
data monitoring and extraction. The assessment should check the
platform's documentation or directly observe the authentication and
renewal process to confirm that token updates do not interrupt or
compromise data access.

-   Yes

-   **No**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

**OC4: Does the platform's API offer an endpoint for extracting data
from an individual publication?**

This item verifies whether it is possible to collect data from a
specific public post on the platform using a unique identifier, rather
than relying on search terms or other filters. The assessment should
review the API documentation and test available endpoints to confirm
that an individual publication can be retrieved directly by its unique
identifier.

-   Yes

-   **No**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

**OC5: Does the platform's API offer an endpoint for extracting data
from an individual author?**

This item verifies whether it is possible to collect data from public
posts made by a specific author, using their username or unique
identifier. The assessment should review the API documentation and test
relevant endpoints to confirm that data can be retrieved directly for an
individual author.

-   Yes

-   **No**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

**OC6: Does the platform's API provide an endpoint for extracting data
based on search terms?**

This item verifies whether public user-generated content can be
collected via individual or combined search terms, enabling the creation
of datasets of posts mentioning those terms. The assessment should test
search-related endpoints to confirm that queries using keywords return
matching public posts.

-   Yes

-   **No**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

**OC7: Does the API use locale-neutral data representations?**

This item verifies whether locale-sensitive data (e.g., timestamps,
currency, numbers) are returned in a locale-neutral format, or whether
relevant locale metadata is included when neutrality is not possible.
The assessment should review the API documentation and inspect sample
responses to confirm the presence of standardized formats or
accompanying metadata.

-   Yes

-   **No**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

### COMPLIANCE

*Compliance refers to how data adheres to standards, conventions and
regulations in a given context. It ensures that data is formatted and
structured in the way it ought to be, according to external or internal
rules.*

**OC8: Does the platform implement a proper deprecation strategy to
avoid breaking client applications while rolling out major changes in
the API?**

This item verifies whether the platform's documentation describes a
deprecation strategy with a grace period before removing features. The
assessment should review changelogs to confirm that deprecated features
are listed with deprecation and removal dates and include migration
instructions. This item applies only to breaking changes that require
client updates, such as endpoint modifications, authentication updates,
or the removal of features.

-   Yes

-   **No or not applicable**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

**OC9: Is the platform's API documentation published in open access?**

This item verifies whether the platform makes its API documentation
openly available on the internet, without requiring registration or
login. The assessment should check whether full documentation can be
accessed freely online without requiring account creation or
authentication.

-   Yes

-   **No**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

**OC10: Is the platform's API documentation clearly written and
exemplified?**

This item verifies whether the documentation for the platform's API is
clear, complete, and provides practical implementation examples. The
assessment should review the documentation to confirm the presence of
detailed explanations, structured references, and sample code or queries
that illustrate correct usage.

-   Yes

-   **No**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

**OC11: Does the platform's API documentation include or link to the API
terms of use?**

This item verifies whether the documentation clearly states or links to
the terms of use governing the API and its legal aspects. The assessment
should review the documentation to confirm the presence of explicit
legal terms that define permitted use and restrictions.

-   Yes

-   **No**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

**OC12: Does the platform's API documentation detail the response format
of each endpoint?**

This item verifies whether the API documentation specifies the response
format for each endpoint, including examples and potential error codes.
The assessment should review the documentation to confirm that, in all
or most cases, response structures are explicitly described and
illustrated with sample outputs.

-   Yes

-   **No**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

**OC13: Does the platform provide its API documentation in the official
languages of the assessed region?**

This item verifies whether the platform provides its API documentation
in the official languages of the assessed region. The assessment should
review the documentation to confirm that complete and up-to-date
versions are available in those languages.

-   Yes

-   **No**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

**OC14: Does the platform's API documentation detail the quota or rate
limits applicable to each available endpoint?**

This item verifies whether the documentation specifies the limits for
each endpoint. Rate limits define the maximum number of requests allowed
within a given period (e.g., 1,000 requests per hour), while quotas set
overall usage limits (e.g., total API calls per month). The assessment
should review the documentation to confirm that usage limits are clearly
stated, including variations by authentication level or endpoint type.

-   Yes

-   **No**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

**OC15: Does the platform provide a way to label content that has been
generated with artificial intelligence?**

This item verifies whether the platform automatically flags, or allows
users to flag, AI-generated content, and whether this information is
given in the API response. The assessment should review the
documentation and test API outputs to confirm that these flags are
included in the extracted data.

-   Yes

-   **No**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

### COMPLETENESS

*Completeness refers to how closely the data reflects the dimensions of
what it represents (in breadth, depth and scope).*

**OC16: Can data from a publication's comments be extracted using the
platform's API?**

This item verifies whether comment data, including their content, can be
extracted when available on the platform, either together with
publication data or with a dedicated endpoint. The assessment should
test relevant endpoints to confirm that comments are retrievable as
structured data. This item does not apply to platforms that do not have
commenting features.

-   Yes

-   **No**

-   Not applicable

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

**OC17: Can data from temporary content be extracted through the
platform's API?**

This item verifies whether the platform's API provides at least one
endpoint for collecting data from temporary publications (e.g., stories,
ephemeral messages). The assessment should test endpoints to confirm
whether this type of short-lived content can be retrieved as structured
data before it expires. This item does not apply to platforms that do
not have temporary content features.

-   Yes

-   **No**

-   Not applicable

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

**OC18: Can historical data be extracted through the platform's API?**

This item verifies whether the API provides endpoints that allow for a
specified time range, going back more than one year from the time the
request is made, to collect public user-generated content data. The
assessment should review test endpoints to confirm that historical data
more than 12 months prior to the analysis can be retrieved.

-   Yes

-   **No**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

**OC19: Is the number of requests allowed by the API sufficient for
monitoring more than 10,000 publications in 24 hours?**

This item verifies whether data can be extracted without interruption
and losses through the platform's API for requests that accumulate more
than 10,000 publications in 24 hours. The assessment should test the API
to confirm that this volume of data can be collected continuously.

-   Yes

-   **No**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

### CONSISTENCY

*This dimension tracks whether the data always presents the same values,
the same format in every occurrence and if it is compatible with the
previous data.*

**OC20: Are the results returned by the API consistently reproducible?**

This item verifies whether data extracted via the platform's API at any
given time is consistent with other collections performed similarly,
including content that has been deleted between collections. The
assessment should conduct repeated test queries to confirm the
reproducibility of results or ground the response based on recent (less
than 2 years) experiments published in peer-reviewed journals.

-   Yes

-   **No**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

**OC21: Is the data returned by the platform's API consistent with the
parameters and filters used in the request?**

This item verifies whether the data extracted through the API accurately
reflects the parameters and filters specified in the request. The
assessment should conduct repeated test queries to confirm the
consistency of results or ground the response based on recent (less than
2 years) experiments published in peer-reviewed journals.

-   Yes

-   **No**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

### RELEVANCE

*Relevance evaluates how helpful the data is and how applicable for use
it is, also considering future applications. This dimension also
evaluates the extent to which the content and coverage of data meet the
user's needs.*

**OC22: Does the data extracted by the platform's API reflect what is
displayed on its user interface?**

This item verifies whether the data returned by the API corresponds to
the information displayed on the platform's user interface at all levels
of detail. The assessment should compare API responses with the user
interface to confirm that key elements, such as authorship, complete
content, interaction counts (e.g., comments, shares, replies), and
referenced content (e.g., shares, mentions), are fully represented.

-   Yes

-   **No**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

**OC23: Does the platform's API allow for filtering data based on
publisher location?**

This item verifies whether the API supports applying location-based
filters to data extraction. The assessment should test the endpoint for
the main content type to confirm that data on public posts can be
filtered by publisher location.

-   Yes

-   **No**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

**OC24: Does the platform's API allow for filtering data based on
content language?**

This item verifies whether the API allows for applying language-based
filters to data extraction. The assessment should test the endpoint for
the main content type to confirm that public post data can be filtered
by content language.

-   Yes

-   **No**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

**OC25: Does the platform's API allow for filtering data by specific
time periods?**

This item verifies whether the API allows applying temporal filters to
data extraction. The assessment should test the endpoint for the main
content type to confirm that public post data can be filtered by custom
time ranges.

-   Yes

-   **No**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

### TIMELINESS

*Timeliness refers to how current and available the data is when it is
requested. Delays in recall render current data useless, as the data is
no longer required.*

**OC26: Can data from newly published content be extracted from the
platform's API in near real time?**

This item verifies whether the API allows the collection of data from
specific content within one hour of its publication. The assessment
should test the endpoint for the main content type to confirm that it
allows the ready extraction of recent public posts data.

-   Yes

-   **No**

**Justification:**

TikTok does not provide an API that enables programmatic access to or
extraction of public user-generated content data for researchers based
in Brazil or affiliated with Brazilian institutions ([[TikTok,
n.d.]{.underline}](https://developers.tiktok.com/products/research-api/)).

REFERENCES
----------

Chemillier, M., Rabearivelo, Y., & Jaylet, R. (2022, May). Observing
Musical Communities Dedicated to Improvisation and Duet Practice on
TikTok Using Web Scraping. In *TikTok-Music-Cultures Perspectives on the
Study of Musicking Practices On & Through TikTok*.
[[https://hal.science/hal-04454074/]{.underline}](https://hal.science/hal-04454074/)

TikTok. (n.d.). *Research Tools*. TikTok for developers.
[[https://developers.tiktok.com/products/research-api/]{.underline}](https://developers.tiktok.com/products/research-api/)
