def test_import_csv_manager():
    import csv_manager
    assert csv_manager is not None


def test_csv_manager_plugin_activation():
    from csv_manager.applications import CSV_MANAGER_APP
    from csv_manager.plugins import csv_manager_plugin

    my_app = CSV_MANAGER_APP()
    app = my_app.app
    app.plugins.activate(["csv_manager_plugin"])
    plugin = app.plugins.get("csv_manager_plugin")
    assert plugin is not None
    assert isinstance(plugin, csv_manager_plugin)
