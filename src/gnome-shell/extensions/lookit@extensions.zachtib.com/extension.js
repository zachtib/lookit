const St = imports.gi.St;
const GLib = imports.gi.GLib;
const Lang = imports.lang;
const PopupMenu = imports.ui.popupMenu;
const PanelMenu = imports.ui.panelMenu;

function LookitMenuItem() {
    this._init.apply(this, arguments);
}

LookitMenuItem.prototype = {
    __proto__: PopupMenu.PopupBaseMenuItem.prototype,

    _init: function(icon, text, menu_icon_first, params) {
        
    },
}

function LookitButton() {
    this._init.apply(this, arguments);
}

LookitButton.prototype = {
    __proto__: PanelMenu.Button.prototype,

    _init: function(mode) {
        PanelMenu.Button.prototype._init.call(this, 0.0);

        this._icon = new St.Icon({ icon_name: 'lookit-dark',
                                   icon_type: St.IconType.FULLCOLOR,
                                   icon_size: Main.panel.button.height });

        this.actor.set_child(this._icon);

        this._menuItem = new PopupMenu.PopupMenuItem('Capture Area');
        this._menuItem.connect('activate', Lang.bind(this, _captureArea));
        this.menu.addMenuItem(this._menuItem)
        
        this._menuItem = new PopupMenu.PopupMenuItem('Capture Active Window');
        this._menuItem.connect('activate', Lang.bind(this, _captureActive));
        this.menu.addMenuItem(this._menuItem)
        
        this._menuItem = new PopupMenu.PopupMenuItem('Capture Screen');
        this._menuItem.connect('activate', Lang.bind(this, _captureScreen));
        this.menu.addMenuItem(this._menuItem)
        
        this._menuItem = new PopupMenu.PopupMenuItem('Preferences');
        this._menuItem.connect('activate', Lang.bind(this, _captureScreen));
        this.menu.addMenuItem(this._menuItem)
        
        this._menuItem = new PopupMenu.PopupMenuItem('About');
        this._menuItem.connect('activate', Lang.bind(this, _captureScreen));
        this.menu.addMenuItem(this._menuItem)

        Main.panel._leftBox.insert_actor(this.actor, 1);
        Main.panel._menus.addMenu(this.menu)
    },

}

function _captureArea() {
    GLib.spawn_command_line_async('lookit --capture-area')
}

function _captureActive() {
    GLib.spawn_command_line_async('lookit --capture-active-window')
}

function _captureScreen() {
    GLib.spawn_command_line_async('lookit --capture-screen')
}

function _preferences() {
    GLib.spawn_command_line_async('lookit --preferences')
}

function _about() {
    GLib.spawn_command_line_async('lookit --about')
}
 
function main(extensionMeta) {
    new LookitButton();
}
