File Format Spec
==============================

Caseversion 
-----------------
```
{
  resource_rui: [full resource uri] //used for diffing and pushing
  (other metadata)
}

TEST THAT [title]
[description]

WHEN [instruction]
THEN [expected]
```

Suite
------------------
```
{
  resource_rui: [full resource uri] //used for diffing and pushing
  other: metadata
}

TEST THAT [title 1]
[description]

WHEN [instruction]
THEN [expected]

===== //separator
{
  resource_rui: [full resource uri] //used for diffing and pushing
  other: metadata
}


TEST THAT [title 2]
[description]

WHEN [instruction]
THEN [expected]

```
