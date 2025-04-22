# Import required packages
from pcse.base import ParameterProvider
from pcse.input import (DummySoilDataProvider, ExcelWeatherDataProvider, WOFOST72SiteDataProvider,
                        YAMLAgroManagementReader, YAMLCropDataProvider)
from pcse.models import Wofost72_PP
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
import yaml

# Set the paths of all input and output files
cwd = Path.cwd()
input_dir = cwd / "input_data"
output_dir = cwd / "output_data"
agro_fp = input_dir / "agro.yaml"
crop_dir = input_dir / "crop"
site_fp = input_dir / "site.yaml"
soil_fp = input_dir / "soil.yaml"
weather_fp = input_dir / "weather_wageningen.xlsx"
output_fp = output_dir / "output.xlsx"
fig_fp = output_dir / "timeplots.jpeg"

# Open the site, soil, and agro files and store the contents in variables
sited = yaml.safe_load(open(site_fp, 'r'))
soild = yaml.safe_load(open(soil_fp, 'r'))
agrod = yaml.safe_load(open(agro_fp, 'r'))
cropd = YAMLCropDataProvider(fpath = crop_dir, force_reload = True)
weatherd = ExcelWeatherDataProvider(weather_fp)

# Combine all input data in a single ParameterProvider object, build a model and run.
parameters = ParameterProvider(cropdata = cropd, sitedata = sited, soildata = soild)
wofost = Wofost72_PP(parameters, weatherd, agrod)
wofost.run_till_terminate()

# Collect simulation output
df = pd.DataFrame(wofost.get_output()).set_index("day")
fig, axs = plt.subplots(nrows = 1, ncols = 2, figsize=(16,8))
df["LAI"].plot(ax=axs[0], label="LAI", color='k')
df["TAGP"].plot(ax=axs[1], label="Total biomass")
df["TWSO"].plot(ax=axs[1], label="Yield")
axs[0].set_title("Leaf Area Index")
axs[1].set_title("Crop biomass")
r = axs[1].legend()
fig.autofmt_xdate()

# Save output
fig.savefig(fig_fp, dpi = 600)
df.to_excel(output_fp)



