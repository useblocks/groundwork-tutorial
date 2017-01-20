CSV Watcher Documentation
=========================

Registered csv watchers: {{ plugin.app.csv_watcher.get()|length}}

Files and versions
------------------
{% for csv_file in plugin.get_csv_history() %}
    {{csv_file.name}}
    {{"~"*csv_file.name|length}}
    {% for version in csv_file.version %}
        **{{version.version}}**

        Missing rows
        ++++++++++++
        {% for missing_row in version.missing_row -%}
            {{missing_row.row}}
        {% endfor -%}

        New rows
        ++++++++
        {% for new_row in version.new_row -%}
            {{new_row.row}}
        {% endfor -%}

    {% endfor %}
{% endfor %}
