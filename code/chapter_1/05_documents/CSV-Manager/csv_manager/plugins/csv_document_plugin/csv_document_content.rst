CSV Watcher Documentation
=========================

Registered csv watchers: {{ plugin.app.csv_watcher.get()|length}}

Files and versions
------------------
{% for key, value in plugin.archive.items() %}
    {{key}}
    {{"~"*key|length}}

    {% for key, value in value["versions"].items() %}
        {{key}}
        Missing: {{value["missing_rows"]}}
        New: {{value["new_rows"]}}
    {% endfor %}
{% endfor %}
