import yaml
import sys
import json

def modify_yaml(input_file, output_file):
    with open(input_file, 'r') as file:
        deploymentconfig = yaml.safe_load(file)

    # Alterações específicas para converter DeploymentConfig em Deployment
    deploymentconfig['apiVersion'] = 'apps/v1'
    deploymentconfig['kind'] = 'Deployment'

    # Remover o bloco metadata.annotations, se existir
    if 'annotations' in deploymentconfig['metadata']:
        del deploymentconfig['metadata']['annotations']

    # Modificar spec.selector para usar matchLabels
    if 'selector' in deploymentconfig['spec']:
        deploymentconfig['spec']['selector'] = {
            'matchLabels': deploymentconfig['spec']['selector']
        }

    # Modificar strategy.type para RollingUpdate
    if 'strategy' in deploymentconfig['spec']:
        deploymentconfig['spec']['strategy']['type'] = 'RollingUpdate'

    # Remover o bloco spec.triggers, se existir
    if 'triggers' in deploymentconfig['spec']:
        del deploymentconfig['spec']['triggers']

    # Remover o bloco status, se existir
    if 'status' in deploymentconfig:
        del deploymentconfig['status']

    with open(output_file, 'w') as file:
        yaml.dump(deploymentconfig, file, default_flow_style=False)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_dc_to_deployment.py <input_yaml> <output_yaml>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    modify_yaml(input_file, output_file)
    print(f"YAML modificado salvo em {output_file}")
