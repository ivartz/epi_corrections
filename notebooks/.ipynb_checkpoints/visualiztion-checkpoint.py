from spimagine import volshow, volfig

def spimagine_show_volume_numpy(numpy_array, stackUnits=(1, 1, 1), interpolation="nearest", cmap="grays"):
    # Spimagine OpenCL volume renderer.
    volfig()
    spim_widget = \
    volshow(numpy_array, stackUnits=stackUnits, interpolation=interpolation)
    spim_widget.set_colormap(cmap)