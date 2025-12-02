**Methodological notes**
========================

We defined public UGC on Telegram as all data accessible to anyone in
public channels or public groups, without requiring approval.

We assessed the Telegram Client API (
[[https://core.telegram.org/\#tdlib-build-your-own-telegram]{.underline}](https://core.telegram.org/#tdlib-build-your-own-telegram)
) using the Python wrapper in October 2025.

**--**
======

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

-   **Yes**

-   Yes, but only for approved researchers

-   No

**Justification:**

The platform offers an API that allows the collection of public data in
Telegram conversations.

[[https://core.telegram.org/]{.underline}](https://core.telegram.org/)

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

In Telegram, public user-generated content (UGC) cannot be globally
discovered or retrieved through the API without prior participation or
explicit identifiers. Users can access content only from channels or
groups where their bot or account is already a member; there is no
mechanism to expose all available channels and groups. There are even
specific error messages for cases where the user is not part of the
supergroup or channel from which data is being requested. Therefore, the
API does not provide membership-free, platform-wide access to the full
set of public UGC.

[[https://core.telegram.org/]{.underline}](https://core.telegram.org/method/channels.getFullChannel)

[[https://core.telegram.org/method/channels.getFullChannel]{.underline}](https://core.telegram.org/method/channels.getFullChannel)

**SC3: Is access to the platform's API free of charge?** - weight 0.30

This item verifies whether API use is free of charge, since even modest
fees can create barriers or force researchers in low-resourced settings
to narrow the scope of their work. The assessment should verify the
platform's documentation and pricing policies to confirm that no fees
are applied for API access.

-   **Yes**

-   Yes, but only for approved researchers

-   No

All Telegram APIs are free of charge:
[[https://core.telegram.org/]{.underline}](https://core.telegram.org/)

--

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

The platform provides no official graphical user interface or tools for
researchers to extract data. All data access is API-based, requiring
technical implementation and programming skills.

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

No official researcher access program exists. Researchers use the same
public APIs as other developers to access publicly available channels
and groups.

--

**OC2: Can the requested data be extracted directly from the platform's
API response?**

This item verifies whether the API returns structured data directly in
its response, rather than only providing a redirect link to the data.
Audiovisual media (e.g., images, videos, and audio) are excluded from
this assessment. The assessment should check sample API responses to
confirm that the requested public data is included in the returned
payload itself.

-   **Yes**

-   No

Responses to requests to the Telegram API provide the expected data in
an appropriate format, without requiring redirection.

--

**OC3: Does the platform's API provide a form of authentication that
allows for token renewal without the risk of data loss?**

This item verifies whether the tokens provided for API use can be
renewed without risk of data loss, ensuring continuity and integrity of
data monitoring and extraction. The assessment should check the
platform's documentation or directly observe the authentication and
renewal process to confirm that token updates do not interrupt or
compromise data access.

-   **Yes**

-   No

Telegram API access requires an access key that remains the same even
after logging in multiple times. It will only change in specific
situations, and the API provides the necessary methods to update it
programmatically.

[[https://core.telegram.org/tdlib/getting-started\#:\~:text=Authorization%20is%20an%20example%20of,description%20of%20the%20current%20AuthorizationState.]{.underline}](https://core.telegram.org/tdlib/getting-started#:~:text=Authorization%20is%20an%20example%20of,description%20of%20the%20current%20AuthorizationState)

**OC4: Does the platform's API offer an endpoint for extracting data
from an individual publication?**

This item verifies whether it is possible to collect data from a
specific public post on the platform using a unique identifier, rather
than relying on search terms or other filters. The assessment should
review the API documentation and test available endpoints to confirm
that an individual publication can be retrieved directly by its unique
identifier.

-   **Yes**

-   No

It is possible to extract data for a specific message using its unique
identifier, as long as the group or public channel it belongs to is
known.

---

**OC5: Does the platform's API offer an endpoint for extracting data
from an individual author?**

This item verifies whether it is possible to collect data from public
posts made by a specific author, using their username or unique
identifier. The assessment should review the API documentation and test
relevant endpoints to confirm that data can be retrieved directly for an
individual author.

-   **Yes**

-   No

Telegram offers a dedicated endpoint for searching for messages by
author, as long as the group or public channel the message belongs to is
known.

[[https://core.telegram.org/method/messages.search]{.underline}](https://core.telegram.org/method/messages.search)

**---**

**OC6: Does the platform's API provide an endpoint for extracting data
based on search terms?**

This item verifies whether public user-generated content can be
collected via individual or combined search terms, enabling the creation
of datasets of posts mentioning those terms. The assessment should test
search-related endpoints to confirm that queries using keywords return
matching public posts.

-   **Yes**

-   No

Telegram offers an endpoint for searching for messages containing terms
of interest, but this is only available in public groups and channels
that the researcher already knows and/or participates in. Supposedly,
Telegram offers a paid tier with global search, but it hasn't been
possible to test it because the evaluation used the free tier across all
platforms.

[[https://core.telegram.org/method/messages.searchGlobal]{.underline}](https://core.telegram.org/method/messages.searchGlobal)

[[https://docs.telethon.dev/en/stable/modules/client.html\#telethon.client.messages.MessageMethods.get\_messages]{.underline}](https://docs.telethon.dev/en/stable/modules/client.html#telethon.client.messages.MessageMethods.get_messages)

---

**OC7: Does the API use locale-neutral data representations?**

This item verifies whether locale-sensitive data (e.g., timestamps,
currency, numbers) are returned in a locale-neutral format, or whether
relevant locale metadata is included when neutrality is not possible.
The assessment should review the API documentation and inspect sample
responses to confirm the presence of standardized formats or
accompanying metadata.

-   **Yes**

-   No

The publication dates returned by the Telegram API follow the ISO 8601
format.

### ---

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

We found no official documentation for TDLib that outlines a deprecation
policy. While there is a changelog on GitHub, it documents only changes
that have already been made to major releases. The document does not
include removal dates and migration instructions for deprecated
features.

[[https://core.telegram.org/tdlib/Change\_Log]{.underline}](https://core.telegram.org/tdlib/Change_Log)

[[https://github.com/tdlib/td/blob/master/CHANGELOG.md]{.underline}](https://github.com/tdlib/td/blob/master/CHANGELOG.md)

[[https://github.com/tdlib/td/issues/3448]{.underline}](https://github.com/tdlib/td/issues/3448)

[[https://github.com/tdlib/td/issues/2215]{.underline}](https://github.com/tdlib/td/issues/2215)

----

**OC9: Is the platform's API documentation published in open access?**

This item verifies whether the platform makes its API documentation
openly available on the internet, without requiring registration or
login. The assessment should check whether full documentation can be
accessed freely online without requiring account creation or
authentication.

-   **Yes**

-   No

Telegram API documentation can be accessed without authentication.
[[https://core.telegram.org/methods]{.underline}](https://core.telegram.org/methods)

--

**OC10: Is the platform's API documentation clearly written and
exemplified?**

This item verifies whether the documentation for the platform's API is
clear, complete, and provides practical implementation examples. The
assessment should review the documentation to confirm the presence of
detailed explanations, structured references, and sample code or queries
that illustrate correct usage.

-   Yes

-   **No**

The Telegram and TDLib API documentation is not clearly written or
exemplified. While it provides a technical reference of available
classes and methods, it lacks detailed explanations and practical
examples demonstrating how to call endpoints or implement typical
workflows. The documentation's structure assumes prior familiarity with
Telegram's internal architecture, making it difficult for developers to
understand usage without relying on third-party resources or community
libraries.

[[https://core.telegram.org/api]{.underline}](https://core.telegram.org/api)

**---\
**

**OC11: Does the platform's API documentation include or link to the API
terms of use?**

This item verifies whether the documentation clearly states or links to
the terms of use governing the API and its legal aspects. The assessment
should review the documentation to confirm the presence of explicit
legal terms that define permitted use and restrictions.

-   **Yes**

-   No

Terms of service are explicitly referenced in API documentation and
required reading for developers obtaining "api\_id" credentials.

[[https://core.telegram.org/api/obtaining\_api\_id]{.underline}](https://core.telegram.org/api/obtaining_api_id)

[[https://core.telegram.org/api/terms]{.underline}](https://core.telegram.org/api/terms)

---

**OC12: Does the platform's API documentation detail the response format
of each endpoint?**

This item verifies whether the API documentation specifies the response
format for each endpoint, including examples and potential error codes.
The assessment should review the documentation to confirm that, in all
or most cases, response structures are explicitly described and
illustrated with sample outputs.

-   Yes

-   **No**

The Telegram TDLib API documentation does not consistently detail the
response format of each endpoint. While it defines object schemas and
return types, it lacks explicit response examples and per-endpoint error
code descriptions.

[[https://core.telegram.org/tdlib/docs/]{.underline}](https://core.telegram.org/tdlib/docs/)

---

**OC13: Does the platform provide its API documentation in the official
languages of the assessed region?**

This item verifies whether the platform provides its API documentation
in the official languages of the assessed region. The assessment should
review the documentation to confirm that complete and up-to-date
versions are available in those languages.

-   Yes

-   **No**

All documentation is exclusively in English.

[[https://core.telegram.org/tdlib/docs/]{.underline}](https://core.telegram.org/tdlib/docs/)

---

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

While Telegram provides information on bot rate limits, the TDLib
documentation does not fully and explicitly detail the quotas or rate
limits for each available endpoint.

[[https://core.telegram.org/bots/faq\#my-bot-is-hitting-limits-how-do-i-avoid-this]{.underline}](https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this)

---

**OC15: Does the platform provide a way to label content that has been
generated with artificial intelligence?**

This item verifies whether the platform automatically flags, or allows
users to flag, AI-generated content, and whether this information is
given in the API response. The assessment should review the
documentation and test API outputs to confirm that these flags are
included in the extracted data.

-   Yes

-   **No**

**Justification:** We found no official policy or technical
specification for AI-generated content in Telegram's API documentation
and terms of service.

---

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

-   **Yes**

-   No

-   Not applicable

Telegram allows extracting comments from channels with discussion
features enabled. Each comment is treated as a reply within a message
thread, which can be retrieved as structured data.

[[https://core.telegram.org/api/discussion\#channel-comments]{.underline}](https://core.telegram.org/api/discussion#channel-comments)

---

**OC17: Can data from temporary content be extracted through the
platform's API?**

This item verifies whether the platform's API provides at least one
endpoint for collecting data from temporary publications (e.g., stories,
ephemeral messages). The assessment should test endpoints to confirm
whether this type of short-lived content can be retrieved as structured
data before it expires. This item does not apply to platforms that do
not have temporary content features.

-   **Yes**

-   No

-   Not applicable

Telegram allows extracting temporary content from groups and channels
while it is still available, even if those messages are configured with
an auto-delete timer. The auto-delete feature only removes messages
after the expiration time, but during their active period, they remain
accessible through the API as regular messages.

[[https://core.telegram.org/method/messages.getHistory]{.underline}](https://core.telegram.org/method/messages.getHistory)

[[https://core.telegram.org/api/stories]{.underline}](https://core.telegram.org/api/stories)

----

**OC18: Can historical data be extracted through the platform's API?**

This item verifies whether the API provides endpoints that allow for a
specified time range, going back more than one year from the time the
request is made, to collect public user-generated content data. The
assessment should test endpoints to confirm that historical data more
than 12 months prior to the analysis can be retrieved.

-   **Yes**

-   No

Telegram's TDLib and core API allow the extraction of historical data
without any fixed time limitation, including content older than one
year.

---

**OC19: Is the number of requests allowed by the API sufficient for
monitoring more than 10,000 publications in 24 hours?**

This item verifies whether data can be extracted without interruption
and losses through the platform's API for requests that accumulate more
than 10,000 publications in 24 hours. The assessment should test the API
to confirm that this volume of data can be collected continuously.

-   **Yes**

-   No

Telegram's API --- including TDLib and the core "messages.\*" methods
--- does not impose strict global rate limits that would prevent
continuous extraction of large message volumes, such as 10,000
publications in 24 hours.

---

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

Because messages can be edited or deleted (including by users, chat
owners, or due to auto-delete settings) and Telegram API treats deleted
messages as if they had never existed, identical queries at different
times may return different results or miss content that has been removed

**OC21: Is the data returned by the platform's API consistent with the
parameters and filters used in the request?**

This item verifies whether the data extracted through the API accurately
reflects the parameters and filters specified in the request. The
assessment should conduct repeated test queries to confirm the
consistency of results or ground the response based on recent (less than
2 years) experiments published in peer-reviewed journals.

-   **Yes**

-   No

Our tests showed that the API results are consistent with the parameters
and filters used in the requests.

---

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

-   **Yes**

-   No

Based on tests carried out, requests to the Telegram API, made at
different times and by different people, return consistent data with
minimal variation, except for publications that have been removed or
made private.

---

**OC23: Does the platform's API allow for filtering data based on
publisher location?**

This item verifies whether the API supports applying location-based
filters to data extraction. The assessment should test the endpoint for
the main content type to confirm that data on public posts can be
filtered by publisher location.

-   Yes

-   **No**

Telegram's TDLib and core API do not provide any parameters or endpoints
that allow filtering messages or posts by the publisher's geographic
location.

**OC24: Does the platform's API allow for filtering data based on
content language?**

This item verifies whether the API allows for applying language-based
filters to data extraction. The assessment should test the endpoint for
the main content type to confirm that public post data can be filtered
by content language.

-   Yes

-   **No**

Telegram's TDLib and core API do not include any parameters or methods
that enable filtering data based on the language of message content.

**OC25: Does the platform's API allow for filtering data by specific
time periods?**

This item verifies whether the API allows applying temporal filters to
data extraction. The assessment should test the endpoint for the main
content type to confirm that public post data can be filtered by custom
time ranges.

-   **Yes**

-   No

Telegram's API, including TDLib, supports filtering data by specific
time periods through parameters that control message retrieval ranges.
The API method "SearchRequest" accepts parameters such as "min\_date"
and "max\_date", allowing clients to retrieve messages within custom
date or ID intervals. Similarly, TDLib's "getChatHistory" method allows
fetching messages before or after a given message ID or timestamp,
enabling temporal filtering.

[[https://core.telegram.org/method/messages.getHistory\#parameters]{.underline}](https://core.telegram.org/method/messages.getHistory#parameters)

[[https://tl.telethon.dev/methods/messages/search.html]{.underline}](https://tl.telethon.dev/methods/messages/search.html)

----

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

-   **Yes**

-   No

Telegram's TDLib and core APIs support near-real-time extraction of
newly published content.

[[https://core.telegram.org/method/messages.getHistory]{.underline}](https://core.telegram.org/method/messages.getHistory)

[[https://core.telegram.org/bots/api\#getupdates]{.underline}](https://core.telegram.org/bots/api#getupdates)
