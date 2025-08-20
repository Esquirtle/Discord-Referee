from discord import ButtonStyle, Interaction, Modal, TextInput
from discord.ui import View

class PanelGenerator:
    @staticmethod
    def create_registration_panel() -> Modal:
        modal = Modal(title="Register")
        username_input = TextInput(label="Username", placeholder="Enter your username", required=True)
        email_input = TextInput(label="Email", placeholder="Enter your email", required=True)
        
        modal.add_item(username_input)
        modal.add_item(email_input)
        
        return modal

    @staticmethod
    def create_team_creation_panel() -> Modal:
        modal = Modal(title="Create Team")
        team_name_input = TextInput(label="Team Name", placeholder="Enter your team name", required=True)
        team_description_input = TextInput(label="Description", placeholder="Enter a description for your team", required=False)
        
        modal.add_item(team_name_input)
        modal.add_item(team_description_input)
        
        return modal

    @staticmethod
    def create_match_join_panel() -> Modal:
        modal = Modal(title="Join Match")
        match_id_input = TextInput(label="Match ID", placeholder="Enter the match ID to join", required=True)
        
        modal.add_item(match_id_input)
        
        return modal

    @staticmethod
    def create_statistics_panel(user_id: str) -> View:
        view = View()
        button = Button(label="View Statistics", style=ButtonStyle.primary)
        
        async def button_callback(interaction: Interaction):
            await interaction.response.send_message(f"Showing statistics for user: {user_id}")
        
        button.callback = button_callback
        view.add_item(button)
        
        return view

    @staticmethod
    def create_profile_modification_panel() -> Modal:
        modal = Modal(title="Modify Profile")
        username_input = TextInput(label="New Username", placeholder="Enter your new username", required=False)
        email_input = TextInput(label="New Email", placeholder="Enter your new email", required=False)
        
        modal.add_item(username_input)
        modal.add_item(email_input)
        
        return modal