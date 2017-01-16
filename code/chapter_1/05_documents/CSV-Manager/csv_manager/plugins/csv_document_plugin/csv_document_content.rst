CSV Watcher Documentation
=========================

Registered csv watchers: {{ plugin.app.csv_watcher.get()|length}}

Files and versions
------------------
{% for key, csv_file in plugin.archive.items() %}
    {{key}}
    {{"~"*key|length}}

    {% for key, version in csv_file["versions"].items() %}
        {{key}}
        Missing: {{version["missing_rows"]}}
        New: {{version["new_rows"]}}
    {% endfor %}
{% endfor %}
